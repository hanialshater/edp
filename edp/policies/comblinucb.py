"""
CombLinUCB — Combinatorial Linear UCB slate bandit.

Per arm (widget) maintain a posterior over a linear coefficient θ_a ∈ R^d
with Gaussian prior (precision λ I). At decision time, compute the upper
confidence bound

  UCB_a(x) = θ̂_a · x + α · sqrt(x^T A_a⁻¹ x)

for every arm a, sort by UCB, and pick the top-K (here K = N_SLOTS = 6).
Update each chosen arm's posterior with the same observed reward (the
slate-bandit signal: the page total). Page-level attribution is the
default — each chosen arm receives `page_total / N_SLOTS` as its
observation, same as our per-slot LinTS in §5.1.

This is the natural combinatorial-bandit baseline for slate problems.
Slate-LinTS (§5.3) is the Thompson-sampling sibling; CombLinUCB
substitutes the upper confidence bound for the TS sample.
"""
from __future__ import annotations
import numpy as np

from edp.config import N_SLOTS
from edp.catalog import N_WIDGETS, WIDGETS
from edp.policies.base import Policy


class CombLinUCB(Policy):
    def __init__(self, ctx_dim: int, alpha: float = 0.3, lam: float = 1.0):
        self.d = ctx_dim
        self.K = N_WIDGETS
        self.alpha = alpha
        self.A = [lam * np.eye(ctx_dim) for _ in range(self.K)]
        self.b = [np.zeros(ctx_dim) for _ in range(self.K)]
        self.A_inv = [np.eye(ctx_dim) / lam for _ in range(self.K)]

    def select_page_with_payload(self, x: np.ndarray):
        ucb = np.full(self.K, -np.inf)
        for a in range(self.K):
            mu = self.A_inv[a] @ self.b[a]
            mean = float(mu @ x)
            # exploration bonus: alpha * sqrt(x' A_inv x)
            bonus = self.alpha * float(np.sqrt(max(x @ self.A_inv[a] @ x, 0.0)))
            ucb[a] = mean + bonus
        # Top-K by UCB
        order = np.argsort(-ucb)[:N_SLOTS]
        page = [WIDGETS[a] for a in order]
        payload = [(int(a), x) for a in order]
        return page, payload

    def select_page(self, feat: dict):
        raise NotImplementedError('Use select_page_with_payload with a context')

    def record_feedback(self, payload, observed_page_reward: float):
        slot_r = observed_page_reward / N_SLOTS
        for a, x in payload:
            self.A[a] += np.outer(x, x)
            self.b[a] += x * slot_r
            Ax = self.A_inv[a] @ x
            denom = 1.0 + float(x @ Ax)
            self.A_inv[a] -= np.outer(Ax, Ax) / denom
