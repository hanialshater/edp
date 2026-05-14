"""
Bayesian-EDP: GAM parameters become learnable with a Gaussian prior
anchored at the LLM agent's most-recent edit values.

Per delayed (page_reward, page, contexts) tuple, we do one SGD step on
the parameters of the chosen widgets, with a Gaussian regularizer toward
the LLM-prior μ. At LLM checkpoints, μ is updated to the agent's new
edit values, and the regularizer recenters.

The "reward predictor" model:
  R̂_i = a + b · Σ_{slot k} score_module(θ_{w_k}, ctx_k)
where (a, b) are scalar calibration constants (also learnable).

Loss per delayed observation:
  L = (R̂_i − R_obs_i)²  +  λ · Σ_θ ((θ − μ_LLM) / σ_LLM)²

Gradient on θ_{w_k} (only chosen widgets get a step):
  ∂L/∂θ = 2 (R̂_i − R_obs_i) · b · ∂score_k/∂θ + 2 λ (θ − μ_LLM) / σ_LLM²

Updates are small (η=1e-3 default) so the prior dominates noise from any
single session, but accumulated bias gets corrected over thousands.
"""
from __future__ import annotations
import copy
import numpy as np

from edp.config import N_SLOTS, PROBLEMS
from edp.policies.edp import EDPPolicy, score_problems, make_modules


class BayesianEDPPolicy(EDPPolicy):
    """EDPPolicy with continuous SGD updates regularized toward an LLM prior."""

    def __init__(self, shapes=None, modules=None, prior_modules=None,
                 lr: float = 1e-3, lam: float = 0.5, prior_sigma: float = 0.5,
                 calib_lr: float = 1e-4):
        super().__init__(shapes=shapes, modules=modules)
        # μ_LLM = the prior-anchor module config
        self.prior_modules = copy.deepcopy(prior_modules or self.modules)
        self.lr = lr
        self.lam = lam
        self.sigma = prior_sigma
        self.calib_lr = calib_lr
        # calibration constants: R̂ = a + b · Σ score_k
        self.a = 0.0
        self.b = 1.0

    # ---------- Update API ----------
    def reset_prior(self, modules):
        """Re-anchor the regularizer at a new LLM-edit point."""
        self.prior_modules = copy.deepcopy(modules)
        # Also reset live modules to the new prior — the agent's edits
        # supersede whatever drift accumulated.
        self.modules = copy.deepcopy(modules)

    def _score_one(self, name: str, remaining: dict, coverage: dict, slot: int) -> float:
        m = self.modules[name]
        s = m['base']
        for p, w in m.get('on_rem', {}).items():
            s += w * remaining.get(p, 0.0)
        for p, w in m.get('on_cov', {}).items():
            s += w * coverage.get(p, 0.0)
        s -= m.get('slot_decay', 0.0) * slot
        return s

    def _replay_compose(self, feat: dict):
        """
        Re-run greedy composition under current modules, returning the
        (page, contexts) needed for SGD: per slot, the (remaining, coverage,
        slot) seen at decision time and the per-slot score.
        """
        problems = score_problems(feat, self.shapes)
        remaining = dict(problems)
        coverage = {p: 0.0 for p in PROBLEMS}
        page, used = [], set()
        contexts = []                 # per-slot snapshot
        scores = []                   # per-slot score under current θ
        for slot in range(N_SLOTS):
            best, best_s = None, -1e9
            for name in self.modules:
                if name in used:
                    continue
                s = self._score_one(name, remaining, coverage, slot)
                if s > best_s:
                    best_s, best = s, name
            page.append(best)
            used.add(best)
            contexts.append({'remaining': dict(remaining),
                              'coverage':  dict(coverage),
                              'slot':      slot})
            scores.append(best_s)
            for p, addr in self.modules[best]['addr'].items():
                remaining[p] = max(0.0, remaining[p] - addr)
                coverage[p] = min(1.0, coverage[p] + addr)
        return page, contexts, scores

    def update_from_delayed(self, payload, observed_reward: float):
        """
        payload: (page, contexts, scores) tuple captured at action time.
        observed_reward: delayed page-level reward (with noise).

        One SGD step on each chosen widget's parameters + (a, b) calibration.
        """
        page, contexts, scores = payload
        score_sum = float(sum(scores))
        # R̂ = a + b · score_sum
        pred = self.a + self.b * score_sum
        residual = pred - observed_reward                    # 2× factor folded into lr
        # Calibration update
        self.a -= self.calib_lr * residual
        self.b -= self.calib_lr * residual * score_sum
        # Per-widget gradient (chain rule through score_module)
        for slot_idx, (w_name, ctx) in enumerate(zip(page, contexts)):
            mod = self.modules[w_name]
            prior = self.prior_modules.get(w_name, mod)
            scale = self.b   # ∂R̂/∂score = b
            # base
            grad_base = residual * scale
            reg_base = (mod['base'] - prior.get('base', mod['base'])) / max(self.sigma**2, 1e-9)
            mod['base'] -= self.lr * (grad_base + self.lam * reg_base)
            # on_rem[p]
            for p in PROBLEMS:
                rem = ctx['remaining'].get(p, 0.0)
                if rem == 0 and p not in mod.get('on_rem', {}):
                    continue
                mod.setdefault('on_rem', {})
                cur = mod['on_rem'].get(p, 0.0)
                mu = prior.get('on_rem', {}).get(p, 0.0)
                grad = residual * scale * rem
                reg = (cur - mu) / max(self.sigma**2, 1e-9)
                new = cur - self.lr * (grad + self.lam * reg)
                if abs(new) > 1e-6 or p in mod['on_rem']:
                    mod['on_rem'][p] = new
            # on_cov[p]
            for p in PROBLEMS:
                cov = ctx['coverage'].get(p, 0.0)
                if cov == 0 and p not in mod.get('on_cov', {}):
                    continue
                mod.setdefault('on_cov', {})
                cur = mod['on_cov'].get(p, 0.0)
                mu = prior.get('on_cov', {}).get(p, 0.0)
                grad = residual * scale * cov
                reg = (cur - mu) / max(self.sigma**2, 1e-9)
                new = cur - self.lr * (grad + self.lam * reg)
                if abs(new) > 1e-6 or p in mod['on_cov']:
                    mod['on_cov'][p] = new
            # slot_decay
            sd = ctx['slot']
            if sd > 0:
                cur = mod.get('slot_decay', 0.0)
                mu = prior.get('slot_decay', cur)
                grad = -residual * scale * sd
                reg = (cur - mu) / max(self.sigma**2, 1e-9)
                mod['slot_decay'] = cur - self.lr * (grad + self.lam * reg)

    def select_page_with_payload(self, feat: dict):
        """Returns (page, payload). Payload is consumed by update_from_delayed."""
        page, contexts, scores = self._replay_compose(feat)
        return page, (page, contexts, scores)
