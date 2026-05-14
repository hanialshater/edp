"""
Per-slot Linear Thompson Sampling.

  - N_SLOTS independent LinTS instances
  - Each instance: K=N_WIDGETS arms, context dim d
  - Action mask prevents repeating a widget within one page
  - update() takes a single (x, a, r); the harness handles delay and
    page-level credit assignment

Two context types:
  - cold: 14 raw signal values (no domain prior)
  - warm: 7 problem-fingerprint values from EDP's Layer 1

The category can optionally be one-hot appended to either context (default off).
"""
from __future__ import annotations
import numpy as np

from edp.config import N_SLOTS, SIGNAL_NAMES, PROBLEMS
from edp.catalog import N_WIDGETS, WIDGETS, CATEGORIES
from edp.policies.base import Policy


def context_cold(feat: dict, category: str | None = None,
                 with_category: bool = False) -> np.ndarray:
    """14-d raw signals, optionally with one-hot category."""
    x = np.array([feat[s] for s in SIGNAL_NAMES], dtype=float)
    if with_category and category is not None:
        oh = np.zeros(len(CATEGORIES))
        oh[CATEGORIES.index(category)] = 1.0
        x = np.concatenate([x, oh])
    return x


def context_warm(feat: dict, shapes, category: str | None = None,
                 with_category: bool = False) -> np.ndarray:
    """7-d problem fingerprint, optionally with one-hot category."""
    from edp.policies.edp import score_problems
    p = score_problems(feat, shapes)
    x = np.array([p[k] for k in PROBLEMS], dtype=float)
    if with_category and category is not None:
        oh = np.zeros(len(CATEGORIES))
        oh[CATEGORIES.index(category)] = 1.0
        x = np.concatenate([x, oh])
    return x


def context_dim(kind: str, with_category: bool = False) -> int:
    base = {'cold': len(SIGNAL_NAMES), 'warm': len(PROBLEMS)}[kind]
    return base + (len(CATEGORIES) if with_category else 0)


class LinTS:
    """Per-arm linear Thompson sampling with Sherman-Morrison updates."""

    def __init__(self, d: int, n_arms: int, alpha: float = 0.3,
                 lam: float = 1.0, seed: int = 0):
        self.d = d
        self.K = n_arms
        self.alpha = alpha
        self.A = [lam * np.eye(d) for _ in range(n_arms)]
        self.b = [np.zeros(d) for _ in range(n_arms)]
        self.A_inv = [np.eye(d) / lam for _ in range(n_arms)]
        self.rng = np.random.default_rng(seed)

    def select(self, x: np.ndarray, allowed_mask: np.ndarray) -> int:
        scores = np.full(self.K, -np.inf)
        for a in range(self.K):
            if not allowed_mask[a]:
                continue
            mu = self.A_inv[a] @ self.b[a]
            try:
                L = np.linalg.cholesky(self.A_inv[a])
                z = self.rng.standard_normal(self.d)
                theta = mu + self.alpha * (L @ z)
            except np.linalg.LinAlgError:
                theta = mu
            scores[a] = float(theta @ x)
        return int(np.argmax(scores))

    def update(self, x: np.ndarray, a: int, r: float):
        self.A[a] += np.outer(x, x)
        self.b[a] += x * r
        Ax = self.A_inv[a] @ x
        denom = 1.0 + float(x @ Ax)
        self.A_inv[a] -= np.outer(Ax, Ax) / denom


class BanditPolicy(Policy):
    """Per-slot LinTS with page-uniqueness masking."""

    def __init__(self, ctx_dim: int, alpha: float = 0.3, lam: float = 1.0,
                 seed: int = 7, credit: str = 'page_div_slots'):
        self.bandits = [LinTS(d=ctx_dim, n_arms=N_WIDGETS, alpha=alpha, lam=lam,
                              seed=seed + s) for s in range(N_SLOTS)]
        self.credit = credit

    def select_page_with_payload(self, x: np.ndarray):
        used = np.zeros(N_WIDGETS, dtype=bool)
        page, slot_choices = [], []
        for slot in range(N_SLOTS):
            a = self.bandits[slot].select(x, ~used)
            page.append(WIDGETS[a])
            slot_choices.append((slot, int(a), x))
            used[a] = True
        return page, slot_choices

    def select_page(self, feat: dict) -> list[str]:
        # Concrete entry point requires the caller to pass a precomputed
        # context. We keep this for Policy interface compliance, but expect
        # callers to use select_page_with_payload directly.
        raise NotImplementedError('Use select_page_with_payload with a context')

    def record_feedback(self, payload, observed_page_reward: float):
        if self.credit == 'page_div_slots':
            slot_r = observed_page_reward / N_SLOTS
            for slot, a, x in payload:
                self.bandits[slot].update(x, a, slot_r)
        else:
            raise ValueError(f'unknown credit scheme: {self.credit}')
