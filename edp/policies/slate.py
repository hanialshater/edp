"""
Slate-LinTS: a single LinTS over 22 widget arms, posterior-mean (or
TS-sampled) ranking picks the top-N_SLOTS = 6.

This is the natural slate-bandit baseline for our setup. Differences
versus the per-slot LinTS in edp.policies.bandit:

  - **One** LinTS instance, not 6 (so per-arm posteriors are pooled
    across slots; sample efficiency is N_SLOTS× higher in principle).
  - The policy treats the slate as the action: rank widgets by posterior
    score, take the top 6 (no re-sampling per slot).
  - The reward update credit is page-level by default (each arm in the
    selected slate receives `page_total / N_SLOTS` as its observed
    reward). This is mathematically the same dilution that per-slot
    LinTS suffers; the slate framing changes WHICH posteriors get
    updated (one per arm, not 6 × per arm), not the per-arm signal.

We expose this as a single Policy with select_page_with_payload /
record_feedback, so existing harness code can call it the same way.
"""
from __future__ import annotations
import numpy as np

from edp.config import N_SLOTS
from edp.catalog import N_WIDGETS, WIDGETS
from edp.policies.base import Policy
from edp.policies.bandit import LinTS


class SlateLinTSPolicy(Policy):
    """One LinTS over 22 arms; top-N_SLOTS by sampled-θ score."""

    def __init__(self, ctx_dim: int, alpha: float = 0.3, lam: float = 1.0,
                 seed: int = 7):
        self.bandit = LinTS(d=ctx_dim, n_arms=N_WIDGETS, alpha=alpha,
                             lam=lam, seed=seed)
        self.K = N_WIDGETS

    def select_page_with_payload(self, x: np.ndarray):
        # Sample one θ per arm, score, take top N_SLOTS.
        scores = np.full(self.K, -np.inf)
        d = self.bandit.d
        for a in range(self.K):
            mu = self.bandit.A_inv[a] @ self.bandit.b[a]
            try:
                L = np.linalg.cholesky(self.bandit.A_inv[a])
                z = self.bandit.rng.standard_normal(d)
                theta = mu + self.bandit.alpha * (L @ z)
            except np.linalg.LinAlgError:
                theta = mu
            scores[a] = float(theta @ x)
        # Top-N_SLOTS selection (ties broken by argsort -> stable)
        order = np.argsort(-scores)[:N_SLOTS]
        page = [WIDGETS[a] for a in order]
        # payload: list of (arm_index, x) for feedback at update time
        payload = [(int(a), x) for a in order]
        return page, payload

    def select_page(self, feat: dict):
        raise NotImplementedError('Use select_page_with_payload with a context')

    def record_feedback(self, payload, observed_page_reward: float):
        slot_r = observed_page_reward / N_SLOTS
        for a, x in payload:
            self.bandit.update(x, a, slot_r)
