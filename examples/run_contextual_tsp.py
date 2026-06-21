from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from semi_bandit_gym import ContextualLCBAgent, ContextualTSPEnv, EdgeOnlyLCBAgent, ExactOracle, run_episode
from semi_bandit_gym.contextual_tsp import ContextualTSPConfig


def summarize(name, trajectory):
    final = trajectory.records[-1]
    print(
        f"{name:14s} "
        f"deployment={final.deployment_expected_cost:.3f} "
        f"oracle={final.oracle_cost:.3f} "
        f"gap={final.deployment_gap:.3f}"
    )


def main():
    config = ContextualTSPConfig(n_nodes=8, horizon=45, noise_std=0.02)

    contextual_env = ContextualTSPEnv(config, seed=41)
    contextual_agent = ContextualLCBAgent(
        feature_dim=contextual_env.feature_dim,
        alpha=0.75,
        seed=5,
    )
    contextual = run_episode(
        contextual_env,
        contextual_agent,
        ExactOracle(contextual_env),
        steps=35,
    )

    edge_env = ContextualTSPEnv(config, seed=41)
    edge_agent = EdgeOnlyLCBAgent(alpha=0.75, seed=5)
    edge_only = run_episode(edge_env, edge_agent, ExactOracle(edge_env), steps=35)

    summarize("contextual_lcb", contextual)
    summarize("edge_only_lcb", edge_only)


if __name__ == "__main__":
    main()
