"""
Per-slot Linear Thompson Sampling bandit.

  - N_SLOTS independent LinTS instances
  - Each instance: K=N_WIDGETS arms, context dim d (7 warm / 14 cold)
  - Action mask prevents repeating a widget within one page
  - update() takes a single (x, a, r) — delay + page-level credit are handled
    by the harness (see DelayedFeedback in sim.py).

Bandit knows nothing about needs, problems, or page composition. It only
sees its context vector and observes per-slot rewards. Under page-level
attribution, the slot reward it sees is page_total / N_SLOTS.
"""
from __future__ import annotations
import numpy as np

from sim import N_SLOTS, N_WIDGETS, WIDGETS, SIGNAL_NAMES


def context_cold(feat: dict) -> np.ndarray:
    """14-d raw signal vector. No domain prior."""
    return np.array([feat[s] for s in SIGNAL_NAMES], dtype=float)


def context_warm(feat: dict, shapes) -> np.ndarray:
    """7-d problem fingerprint — uses Layer 1 of EDP as a featurizer."""
    from policy_edp import score_problems, PROBLEMS
    p = score_problems(feat, shapes)
    return np.array([p[k] for k in PROBLEMS], dtype=float)


class LinTS:
    """Per-arm linear Thompson sampling with Sherman-Morrison updates."""

    def __init__(self, d: int, n_arms: int, alpha: float = 0.3, lam: float = 1.0, seed: int = 0):
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


class BanditPolicy:
    """
    Per-slot LinTS over the widget catalog with page-uniqueness masking.

    The harness is responsible for:
      - Computing the context (warm/cold) before select_page
      - Routing the delayed page-level reward back via record_feedback

    record_feedback receives (slot_payload, observed_page_reward); we apply
    page_reward / N_SLOTS as the slot credit (equal credit assignment under
    page-level attribution).
    """

    def __init__(self, ctx_dim: int, alpha: float = 0.3, lam: float = 1.0, seed: int = 7,
                 credit: str = 'page_div_slots'):
        self.bandits = [LinTS(d=ctx_dim, n_arms=N_WIDGETS, alpha=alpha, lam=lam, seed=seed + s)
                        for s in range(N_SLOTS)]
        self.credit = credit  # how to split page reward among slots

    def select_page_with_payload(self, x: np.ndarray):
        """Returns (page_widgets, payload_for_feedback)."""
        used = np.zeros(N_WIDGETS, dtype=bool)
        page, slot_choices = [], []
        for slot in range(N_SLOTS):
            a = self.bandits[slot].select(x, ~used)
            page.append(WIDGETS[a])
            slot_choices.append((slot, int(a), x))
            used[a] = True
        return page, slot_choices

    def record_feedback(self, payload, observed_page_reward: float):
        if self.credit == 'page_div_slots':
            slot_r = observed_page_reward / N_SLOTS
            for slot, a, x in payload:
                self.bandits[slot].update(x, a, slot_r)
        else:
            raise ValueError(f'unknown credit scheme: {self.credit}')
