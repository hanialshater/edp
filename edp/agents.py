"""Agent adapters + the canonical episode runner for PageCompositionEnv.

The existing policies have three different shapes:

  - bandits (BanditPolicy, SlateLinTSPolicy, CombLinUCB): act on a
    context *vector* via select_page_with_payload(x), learn via
    record_feedback(payload, reward);
  - EDPPolicy: acts on the raw feat dict via select_page(feat), learns
    only out-of-band via apply_edit_batch(edits) at checkpoints;
  - BayesianEDPPolicy: acts on the raw feat dict via
    select_page_with_payload(feat), learns online via
    update_from_delayed(payload, reward).

The Agent protocol unifies them behind act()/learn()/maybe_checkpoint()
so one runner drives any of them against the same environment.
"""
from __future__ import annotations
from typing import Any, Protocol

import numpy as np

from edp.env import PageCompositionEnv, Observation
from edp.policies.edp import (EDPPolicy, make_problem_shapes, apply_edits,
                              load_edits_json)
from edp.policies.bandit import context_warm, context_cold


class Agent(Protocol):
    def act(self, obs: Observation) -> tuple[list[str], Any]:
        """Return (page, payload). payload is opaque and handed back to learn()."""
        ...

    def learn(self, observed_reward: float, payload: Any) -> None:
        """Consume one matured delayed-feedback item. Default no-op."""
        ...

    def maybe_checkpoint(self, index: int) -> None:
        """Apply any scheduled offline update (e.g. agent edit batch)."""
        ...


# ---------------------------------------------------------------------------
class EDPAgent:
    """Wraps EDPPolicy. Learns only at checkpoints, via edit batches.

    `schedule` maps session index -> edit batch (list of edit dicts/tuples),
    or session index -> path to an edits JSON file."""

    def __init__(self, policy: EDPPolicy | None = None,
                 schedule: dict[int, Any] | None = None):
        self.policy = policy or EDPPolicy()
        self.schedule = schedule or {}

    def act(self, obs: Observation):
        return self.policy.select_page(obs.feat), None

    def learn(self, observed_reward: float, payload: Any) -> None:
        return  # deterministic between checkpoints

    def maybe_checkpoint(self, index: int) -> None:
        if index in self.schedule:
            batch = self.schedule[index]
            if isinstance(batch, str):
                batch = load_edits_json(batch)[0]
            self.policy.apply_edit_batch(batch)


# ---------------------------------------------------------------------------
class BanditAgent:
    """Wraps any bandit policy with a select_page_with_payload(x) /
    record_feedback(payload, reward) interface. Owns the context transform
    so the environment never needs to know about featurisation."""

    def __init__(self, policy, context: str = 'warm', with_category: bool = False):
        self.policy = policy
        self.with_category = with_category
        self._shapes = make_problem_shapes() if context == 'warm' else None
        if context == 'warm':
            self._ctx = lambda feat, cat: context_warm(
                feat, self._shapes, cat, with_category=with_category)
        elif context == 'cold':
            self._ctx = lambda feat, cat: context_cold(
                feat, cat, with_category=with_category)
        else:
            raise ValueError(f'unknown context: {context}')

    def act(self, obs: Observation):
        x = self._ctx(obs.feat, obs.category)
        return self.policy.select_page_with_payload(x)

    def learn(self, observed_reward: float, payload: Any) -> None:
        self.policy.record_feedback(payload, observed_reward)

    def maybe_checkpoint(self, index: int) -> None:
        return


# ---------------------------------------------------------------------------
class BayesianEDPAgent:
    """Wraps BayesianEDPPolicy. Acts on the raw feat dict, learns online
    via update_from_delayed, and re-anchors its prior at checkpoints when
    a schedule of edit batches is supplied."""

    def __init__(self, policy, schedule: dict[int, Any] | None = None):
        self.policy = policy
        self.schedule = schedule or {}

    def act(self, obs: Observation):
        return self.policy.select_page_with_payload(obs.feat)

    def learn(self, observed_reward: float, payload: Any) -> None:
        self.policy.update_from_delayed(payload, observed_reward)

    def maybe_checkpoint(self, index: int) -> None:
        if index in self.schedule:
            batch = self.schedule[index]
            if isinstance(batch, str):
                batch = load_edits_json(batch)[0]
            new_modules = apply_edits(self.policy.modules, [
                (e['widget'], e['path'], e.get('from', 0.0),
                 e['to'], e.get('reason', '')) for e in batch
            ])
            self.policy.reset_prior(new_modules)


# ---------------------------------------------------------------------------
def run_episode(env: PageCompositionEnv, agent: Agent) -> dict:
    """Drive one agent through one full episode of the environment.

    Returns a dict with rewards, oracles, cumulative regret, and the
    headline regret-percent metric."""
    obs = env.reset()
    while obs is not None:
        agent.maybe_checkpoint(obs.index)
        page, payload = agent.act(obs)
        step = env.step(page, payload)
        for r_obs, pl in step.matured:
            agent.learn(r_obs, pl)
        obs = step.obs
    for r_obs, pl in env.drain():
        agent.learn(r_obs, pl)
    return {
        'rewards': env.rewards,
        'oracles': env.oracles,
        'cumulative_regret': env.cumulative_regret(),
        'regret_pct': env.regret_pct(),
    }
