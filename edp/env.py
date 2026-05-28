"""Gym-like environment for whole-page composition.

Separates the *environment* (session stream + ground-truth reward + the
production reward stack: page-level attribution, multi-day delay, noise)
from the *algorithm* (any page-composition policy).

The classic Gym `reset()` / `step()` contract is adapted for delayed
reward. `step(page, payload)` advances one session and returns a
`StepResult` whose `matured` field carries the (noisy, delayed) feedback
that became available at this tick — exactly the feedback a learner is
allowed to see in production. The immediate noise-free reward and the
oracle are returned too, but only for evaluation; a policy that consumes
them is cheating.

Typical loop (see edp/agents.py:run_episode for the canonical runner):

    env = PageCompositionEnv(n=10_000, seed=42, source='parametric')
    obs = env.reset()
    while obs is not None:
        page, payload = agent.act(obs)
        step = env.step(page, payload)
        for r_obs, pl in step.matured:
            agent.learn(r_obs, pl)
        obs = step.obs
    for r_obs, pl in env.drain():        # flush the delay queue
        agent.learn(r_obs, pl)
    loss_pct = env.regret_pct()
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable

import numpy as np

from edp.sim import make_session_stream, DelayedFeedback
from edp.ground_truth import set_source, true_page_reward, oracle_reward


@dataclass(frozen=True)
class Observation:
    """What the policy sees each tick. Persona is deliberately hidden —
    it is the latent the reward depends on, and no policy may read it."""
    index: int        # session index in the stream
    category: str     # fashion category being viewed (observable)
    feat: dict        # 14 raw behavioural signals + price_norm


@dataclass
class StepResult:
    obs: Observation | None              # next observation, None when done
    matured: list[tuple[float, Any]]     # (observed_reward, payload) ready now
    true_reward: float                   # immediate noise-free reward (eval only)
    oracle: float                        # oracle reward for this session (eval only)
    done: bool
    info: dict = field(default_factory=dict)


class PageCompositionEnv:
    """Gym-like environment wrapping the session stream + production
    reward stack. Policy-agnostic: it submits a scalar page reward to the
    delay queue and surfaces matured (reward, payload) pairs; how that
    reward is attributed across slots lives entirely in the policy's
    payload, so per-slot and page-level learners share one environment."""

    def __init__(self, n: int = 10_000, seed: int = 42, *,
                 source: str = 'parametric',
                 delay: int = 500, noise_sigma: float = 0.20,
                 feedback_seed: int | None = None,
                 reward_fn: Callable[[str, str, list[str]], float] | None = None,
                 oracle_fn: Callable[[str, str], float] | None = None):
        set_source(source)
        self.n = n
        self.seed = seed
        self.source = source
        self.delay = delay
        self.noise_sigma = noise_sigma
        self._feedback_seed = feedback_seed if feedback_seed is not None else seed * 7 + 1
        self._reward_fn = reward_fn or true_page_reward
        self._oracle_fn = oracle_fn or oracle_reward
        self._stream: list[tuple[str, str, dict]] = []
        self._fb: DelayedFeedback | None = None
        self._i = 0
        self._rewards: list[float] = []
        self._oracles: list[float] = []
        self._oracle_cache: dict[tuple[str, str], float] = {}

    # ------------------------------------------------------------------
    def reset(self) -> Observation:
        self._stream = make_session_stream(self.n, seed=self.seed)
        self._fb = DelayedFeedback(delay=self.delay, noise_sigma=self.noise_sigma,
                                   seed=self._feedback_seed)
        self._i = 0
        self._rewards = []
        self._oracles = []
        return self._obs(0)

    def step(self, page: list[str], payload: Any = None) -> StepResult:
        if self._fb is None:
            raise RuntimeError('call reset() before step()')
        persona, category, _ = self._stream[self._i]

        # matured feedback that becomes visible at this tick
        matured = list(self._fb.drain_ready(self._i))

        true_r = self._reward_fn(persona, category, page)
        oracle = self._oracle(persona, category)
        self._rewards.append(true_r)
        self._oracles.append(oracle)

        # submit this action's reward to the delay queue with its payload
        if payload is not None:
            self._fb.submit(self._i, true_r, payload)

        self._i += 1
        done = self._i >= self.n
        nxt = None if done else self._obs(self._i)
        return StepResult(obs=nxt, matured=matured, true_reward=true_r,
                          oracle=oracle, done=done,
                          info={'persona': persona, 'category': category})

    def drain(self) -> list[tuple[float, Any]]:
        """Flush the delay queue at end of episode. Returns the residual
        matured feedback the policy still needs to learn from."""
        if self._fb is None:
            return []
        return list(self._fb.drain_all())

    # ------------------------------------------------------------------
    def _obs(self, i: int) -> Observation:
        _, category, feat = self._stream[i]
        return Observation(index=i, category=category, feat=feat)

    def _oracle(self, persona: str, category: str) -> float:
        key = (persona, category)
        if key not in self._oracle_cache:
            self._oracle_cache[key] = self._oracle_fn(persona, category)
        return self._oracle_cache[key]

    # ------------------------------------------------------------------
    def cumulative_regret(self) -> float:
        return float(np.sum(np.array(self._oracles) - np.array(self._rewards)))

    def oracle_total(self) -> float:
        return float(np.sum(self._oracles))

    def regret_pct(self) -> float:
        """Percent of oracle reward lost over the episode — the paper's
        headline metric."""
        tot = self.oracle_total()
        return 100.0 * self.cumulative_regret() / tot if tot else 0.0

    @property
    def rewards(self) -> np.ndarray:
        return np.array(self._rewards)

    @property
    def oracles(self) -> np.ndarray:
        return np.array(self._oracles)
