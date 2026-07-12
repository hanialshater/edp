"""Pooled LinTS with uniform page-level credit.

A single contextual Thompson-sampling model is maintained per widget. At each
round the policy samples one score per widget and selects the top six distinct
widgets. Every selected widget is then updated with ``page_reward / 6``.

This is a useful pooled-arm baseline, but it is *not* a full-bandit slate
algorithm: uniform credit is an attribution heuristic and does not infer the
contribution of the selected set from the scalar page reward. The explicit
name and documentation matter because calling this a generic "slate LinTS"
would overstate the strength of the comparator.

``SlateLinTSPolicy`` is retained as a backwards-compatible alias for existing
experiment scripts and result files.
"""
from __future__ import annotations

import numpy as np

from edp.config import N_SLOTS
from edp.catalog import N_WIDGETS, WIDGETS
from edp.policies.base import Policy
from edp.policies.bandit import LinTS


class PooledLinTSPolicy(Policy):
    """One LinTS model per widget; top-K selection and uniform page credit."""

    def __init__(self, ctx_dim: int, alpha: float = 0.3, lam: float = 1.0,
                 seed: int = 7):
        self.bandit = LinTS(
            d=ctx_dim,
            n_arms=N_WIDGETS,
            alpha=alpha,
            lam=lam,
            seed=seed,
        )
        self.K = N_WIDGETS

    def select_page_with_payload(self, x: np.ndarray):
        scores = np.full(self.K, -np.inf)
        d = self.bandit.d
        for arm in range(self.K):
            mean = self.bandit.A_inv[arm] @ self.bandit.b[arm]
            try:
                chol = np.linalg.cholesky(self.bandit.A_inv[arm])
                theta = mean + self.bandit.alpha * (
                    chol @ self.bandit.rng.standard_normal(d)
                )
            except np.linalg.LinAlgError:
                theta = mean
            scores[arm] = float(theta @ x)

        order = np.argsort(-scores)[:N_SLOTS]
        page = [WIDGETS[arm] for arm in order]
        payload = [(int(arm), x) for arm in order]
        return page, payload

    def select_page(self, feat: dict):
        raise NotImplementedError('Use select_page_with_payload with a context')

    def record_feedback(self, payload, observed_page_reward: float):
        attributed_reward = observed_page_reward / N_SLOTS
        for arm, x in payload:
            self.bandit.update(x, arm, attributed_reward)


# Backwards compatibility for committed scripts and result provenance.
SlateLinTSPolicy = PooledLinTSPolicy
