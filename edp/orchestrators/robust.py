"""
Robust EDP orchestrator.

Wraps the report-based orchestrator with a robustness check after each
agent edit batch:

  1. Agent reads the diagnostic report and proposes edits.
  2. Apply the edits to produce config C_0.
  3. Generate K perturbations of C_0: for each numeric value in the modules
     dict that the edits TOUCHED (transitively, including base/on_rem/on_cov/
     slot_decay), add Gaussian noise sigma=`perturb_sigma`.
  4. Evaluate each candidate (C_0 and the K perturbations) on a held-out
     500-session validation stream (different seed from the live stream).
  5. Pick the candidate that maximises (mean_reward - lambda * std_reward),
     i.e. a risk-adjusted score.
  6. Adopt that candidate as the new state.

Net effect: the curves the agent proposes get pressure-tested against
small parameter noise before going live. If the agent's pick is fragile,
a nearby less-aggressive perturbation wins.
"""
from __future__ import annotations
import copy
import json
import numpy as np

from edp import (make_session_stream, true_page_reward, oracle_reward,
                 EDPPolicy)
from edp.policies.edp import apply_edits, make_modules
from edp.orchestrators.report import ReportOrchestrator, AGENT_PROMPT_TEMPLATE, cli_main


VALIDATION_SEED = 99991
VALIDATION_N = 500


def _walk_numeric(d, path=''):
    """Yield (dotted_path, value) for every numeric leaf in a nested dict."""
    for k, v in d.items():
        sub = f'{path}.{k}' if path else k
        if isinstance(v, dict):
            yield from _walk_numeric(v, sub)
        elif isinstance(v, (int, float)):
            yield sub, float(v)


def _set_dot(d, path, value):
    parts = path.split('.')
    cur = d
    for p in parts[:-1]:
        cur = cur[p]
    cur[parts[-1]] = value


def _touched_params(edits):
    """Return the set of (widget, dotted_path) tuples the edits modify."""
    out = set()
    for e in edits:
        if isinstance(e, dict):
            w, p = e['widget'], e['path']
        else:
            w, p = e[0], e[1]
        out.add((w, p))
    return out


def perturb_config(modules, touched, rng, sigma):
    """Return a new modules dict with Gaussian noise on touched params."""
    out = copy.deepcopy(modules)
    for w, p in touched:
        if w not in out:
            continue
        # If path doesn't exist (new on_cov field) skip — already created
        # by apply_edits before this is called.
        parts = p.split('.')
        cur = out[w]
        ok = True
        for part in parts[:-1]:
            if part not in cur:
                ok = False
                break
            cur = cur[part]
        if not ok or parts[-1] not in cur:
            continue
        v = float(cur[parts[-1]])
        # No-perturb for slot_decay (small values, structural)
        if parts[-1] == 'slot_decay':
            continue
        cur[parts[-1]] = v + float(rng.normal(0.0, sigma))
    return out


def evaluate_config(modules, validation_stream, oracle_vals):
    """Mean reward and std reward of EDPPolicy(modules) on the validation stream."""
    pol = EDPPolicy(modules=modules)
    rewards = np.zeros(len(validation_stream))
    for i, (p, c, f) in enumerate(validation_stream):
        rewards[i] = true_page_reward(p, c, pol.select_page(f))
    return float(rewards.mean()), float(rewards.std())


class RobustOrchestrator(ReportOrchestrator):
    """ReportOrchestrator + post-edit perturbation selection."""

    def __init__(self, state_dir: str, k_perturbations: int = 8,
                 perturb_sigma: float = 0.15, risk_lambda: float = 0.5):
        super().__init__(state_dir)
        self.k = k_perturbations
        self.sigma = perturb_sigma
        self.risk_lambda = risk_lambda

    def apply_edits_from_file(self, state, path, **extras):
        """Override: after applying edits, run perturbation selection."""
        with open(path) as f:
            data = json.load(f)
        edits = data['edits']
        touched = _touched_params(edits)

        # Apply edits to get baseline config C_0
        edit_tuples = [
            (e['widget'], e['path'], e.get('from', 0.0),
             e['to'], e.get('reason', ''))
            for e in edits
        ]
        c0 = apply_edits(state['modules'], edit_tuples)

        # Build validation stream (different seed from live stream)
        val_stream = make_session_stream(VALIDATION_N, seed=VALIDATION_SEED)
        oracle_vals = np.array([oracle_reward(p, c) for p, c, _ in val_stream])

        # Score C_0 and K perturbations
        rng = np.random.default_rng(hash((path, 'robust')) & 0xffffffff)
        candidates = [('baseline', c0)]
        for i in range(self.k):
            candidates.append((f'perturb{i + 1}',
                               perturb_config(c0, touched, rng, self.sigma)))

        scored = []
        for name, cfg in candidates:
            m, s = evaluate_config(cfg, val_stream, oracle_vals)
            # Risk-adjusted score: higher mean, lower std
            score = m - self.risk_lambda * s
            scored.append((score, m, s, name, cfg))

        scored.sort(key=lambda x: -x[0])
        best_score, best_m, best_s, best_name, best_cfg = scored[0]

        # Diagnostic info to log
        all_means = [m for _, m, _, _, _ in scored]
        diag = {
            'baseline_mean': next(m for _, m, _, n, _ in scored if n == 'baseline'),
            'baseline_std':  next(s for _, _, s, n, _ in scored if n == 'baseline'),
            'best_mean':     best_m,
            'best_std':      best_s,
            'best_name':     best_name,
            'mean_range':    [float(min(all_means)), float(max(all_means))],
            'k_perturbations': self.k,
            'perturb_sigma':   self.sigma,
        }

        state['modules'] = best_cfg
        state['edit_history'].append({
            'session': state['session_idx'],
            'count': len(edit_tuples),
            'note': data.get('note', ''),
            'robust_diag': diag,
        })
        return state


if __name__ == '__main__':
    cli_main(RobustOrchestrator)
