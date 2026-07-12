"""Pooled LinUCB with uniform page-level credit.

For each widget, maintain an independent contextual linear UCB model. Select
the six widgets with the largest UCB scores, then update every selected widget
with ``page_reward / 6``.

This is *not* a standard full-bandit combinatorial linear UCB algorithm. The
scalar page reward is not decomposed or estimated jointly over the selected
set; it is copied uniformly to the selected widget models. The implementation
is retained because it is a useful attribution-heuristic baseline, but the
paper must not cite it as evidence against the broader class of combinatorial
full-bandit methods.

``CombLinUCB`` remains as a backwards-compatible alias for existing experiment
scripts and result files.
"""
from __future__ import annotations

import numpy as np

from edp.config import N_SLOTS
from edp.catalog import N_WIDGETS, WIDGETS
from edp.policies.base import Policy


class PooledLinUCB(Policy):
    """Independent per-widget LinUCB models with top-K selection."""

    def __init__(self, ctx_dim: int, alpha: float = 0.3, lam: float = 1.0):
        if lam <= 0:
            raise ValueError('lam must be positive')
        self.d = ctx_dim
        self.K = N_WIDGETS
        self.alpha = alpha
        self.A = [lam * np.eye(ctx_dim) for _ in range(self.K)]
        self.b = [np.zeros(ctx_dim) for _ in range(self.K)]
        self.A_inv = [np.eye(ctx_dim) / lam for _ in range(self.K)]

    def select_page_with_payload(self, x: np.ndarray):
        ucb = np.full(self.K, -np.inf)
        for arm in range(self.K):
            mean_vector = self.A_inv[arm] @ self.b[arm]
            mean = float(mean_vector @ x)
            variance = max(float(x @ self.A_inv[arm] @ x), 0.0)
            ucb[arm] = mean + self.alpha * np.sqrt(variance)

        order = np.argsort(-ucb)[:N_SLOTS]
        page = [WIDGETS[arm] for arm in order]
        payload = [(int(arm), x) for arm in order]
        return page, payload

    def select_page(self, feat: dict):
        raise NotImplementedError('Use select_page_with_payload with a context')

    def record_feedback(self, payload, observed_page_reward: float):
        attributed_reward = observed_page_reward / N_SLOTS
        for arm, x in payload:
            self.A[arm] += np.outer(x, x)
            self.b[arm] += x * attributed_reward
            ax = self.A_inv[arm] @ x
            denominator = 1.0 + float(x @ ax)
            self.A_inv[arm] -= np.outer(ax, ax) / denominator


# Backwards compatibility for committed scripts and result provenance.
CombLinUCB = PooledLinUCB
