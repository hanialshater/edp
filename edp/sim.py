"""
Session stream and delayed-reward queue.

A session is a tuple (persona, category, feat):
  - persona: identifier of the customer archetype (mixture draw)
  - category: fashion category being viewed (independent mixture draw)
  - feat: 14 raw behaviour signals + 1 product feature (price_norm)

The persona source is plug-in: switch with set_source() in edp.ground_truth
or env var EDP_PERSONA_SOURCE in {parametric, llm}.
"""
from __future__ import annotations
import numpy as np
from collections import deque
from dataclasses import dataclass, field

from edp.ground_truth import get_source
from edp.catalog import CATEGORIES, CATEGORY_MIX


def make_session_stream(n: int, seed: int = 42) -> list[tuple[str, str, dict]]:
    """Reproducible (persona, category, feat) stream from the active source."""
    src = get_source()
    p_names = src.persona_names()
    p_w = src.mixture_weights()
    p_probs = np.array([p_w[k] for k in p_names])
    p_probs /= p_probs.sum()

    c_names = CATEGORIES
    c_probs = np.array([CATEGORY_MIX[k] for k in c_names])
    c_probs /= c_probs.sum()

    r = np.random.default_rng(seed)
    stream = []
    for _ in range(n):
        pn = r.choice(p_names, p=p_probs)
        cn = r.choice(c_names, p=c_probs)
        feat = src.sample_session(r, pn)
        stream.append((pn, cn, feat))
    return stream


@dataclass
class DelayedFeedback:
    """
    Submit (session_idx, true_reward, payload) at action time; receive
    (true_reward + Gaussian noise, payload) once session_idx_now >=
    submit_idx + delay. Drain residual queue at end of run.
    """
    delay: int
    noise_sigma: float = 0.0
    seed: int = 0
    _q: deque = field(default_factory=deque)
    _rng: np.random.Generator = field(init=False)

    def __post_init__(self):
        self._rng = np.random.default_rng(self.seed)

    def submit(self, session_idx: int, true_reward: float, payload):
        self._q.append((session_idx, true_reward, payload))

    def drain_ready(self, current_idx: int):
        while self._q and self._q[0][0] + self.delay <= current_idx:
            _, r_true, payload = self._q.popleft()
            r_obs = r_true + (self._rng.normal(0.0, self.noise_sigma)
                              if self.noise_sigma > 0 else 0.0)
            yield r_obs, payload

    def drain_all(self):
        while self._q:
            _, r_true, payload = self._q.popleft()
            r_obs = r_true + (self._rng.normal(0.0, self.noise_sigma)
                              if self.noise_sigma > 0 else 0.0)
            yield r_obs, payload
