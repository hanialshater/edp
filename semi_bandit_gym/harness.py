from __future__ import annotations

from .contextual_tsp import ContextualTSPEnv, ExactOracle
from .types import StepRecord, Trajectory


def run_episode(
    env: ContextualTSPEnv,
    agent,
    evaluator: ExactOracle,
    steps: int,
) -> Trajectory:
    """Run an agent without allowing the agent to access evaluator-only truth."""

    observation = env.reset()
    records: list[StepRecord] = []

    for _ in range(steps):
        exploratory_action = agent.plan(observation)
        result = env.step(exploratory_action)
        agent.update(result.feedback)

        deployment_action = agent.deploy(result.observation)
        exploratory_metrics = evaluator.evaluate(exploratory_action)
        deployment_metrics = evaluator.evaluate(deployment_action)

        records.append(
            StepRecord(
                day=result.observation.day,
                exploration_expected_cost=exploratory_metrics.expected_cost,
                deployment_expected_cost=deployment_metrics.expected_cost,
                oracle_cost=deployment_metrics.oracle_cost,
                deployment_gap=deployment_metrics.gap_to_oracle,
                observed_route_cost=result.route_cost,
            )
        )
        observation = result.observation
        if result.terminated or result.truncated:
            break

    return Trajectory(tuple(records))
