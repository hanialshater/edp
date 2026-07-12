from __future__ import annotations

import unittest

from semi_bandit_gym import (
    ContextualLCBAgent,
    ContextualTSPEnv,
    EdgeOnlyLCBAgent,
    ExactOracle,
    TourAction,
    run_episode,
)
from semi_bandit_gym.contextual_tsp import ContextualTSPConfig
from semi_bandit_gym.solver import brute_force_time_indexed_tsp, solve_time_indexed_tsp


class ContextualTSPContractTests(unittest.TestCase):
    def test_feedback_contains_exactly_the_selected_edges(self) -> None:
        env = ContextualTSPEnv(ContextualTSPConfig(n_nodes=8, noise_std=0.0), seed=7)
        env.reset()
        action = TourAction((0, 1, 2, 3, 4, 5, 6, 7))
        result = env.step(action)

        self.assertEqual(len(result.feedback), 8)
        self.assertEqual(
            {item.edge for item in result.feedback},
            {
                (0, 1),
                (1, 2),
                (2, 3),
                (3, 4),
                (4, 5),
                (5, 6),
                (6, 7),
                (0, 7),
            },
        )
        self.assertFalse(hasattr(result.observation, "true_cost"))
        self.assertFalse(hasattr(result.feedback[0], "expected_cost"))

    def test_invalid_tours_are_rejected(self) -> None:
        env = ContextualTSPEnv(ContextualTSPConfig(n_nodes=6), seed=11)
        env.reset()
        with self.assertRaises(ValueError):
            env.step(TourAction((0, 1, 2, 3, 4, 4)))
        with self.assertRaises(ValueError):
            env.step(TourAction((1, 0, 2, 3, 4, 5)))

    def test_static_hidden_world_has_no_daily_drift(self) -> None:
        env = ContextualTSPEnv(ContextualTSPConfig(n_nodes=6, noise_std=0.0), seed=19)
        env.reset()
        action = TourAction((0, 1, 2, 3, 4, 5))
        first = env.step(action)
        second = env.step(action)

        self.assertEqual(
            [round(item.observed_cost, 10) for item in first.feedback],
            [round(item.observed_cost, 10) for item in second.feedback],
        )

    def test_exact_oracle_matches_bruteforce_reference(self) -> None:
        env = ContextualTSPEnv(ContextualTSPConfig(n_nodes=7, noise_std=0.0), seed=3)
        env.reset()
        oracle = ExactOracle(env)
        exact = solve_time_indexed_tsp(
            env.n_nodes,
            lambda position, left, right: env._hidden_expected_cost(left, right, position),
            start=0,
        )
        brute_force = brute_force_time_indexed_tsp(
            env.n_nodes,
            lambda position, left, right: env._hidden_expected_cost(left, right, position),
            start=0,
        )
        self.assertAlmostEqual(
            env._expected_action_cost(exact),
            env._expected_action_cost(brute_force),
            places=10,
        )
        self.assertAlmostEqual(oracle.cost, env._expected_action_cost(brute_force), places=10)

    def test_contextual_agent_beats_edge_only_after_shared_learning(self) -> None:
        config = ContextualTSPConfig(n_nodes=8, horizon=45, noise_std=0.02)
        contextual_env = ContextualTSPEnv(config, seed=41)
        edge_only_env = ContextualTSPEnv(config, seed=41)

        contextual = ContextualLCBAgent(feature_dim=contextual_env.feature_dim, seed=5, alpha=0.75)
        edge_only = EdgeOnlyLCBAgent(seed=5, alpha=0.75)

        contextual_trajectory = run_episode(contextual_env, contextual, ExactOracle(contextual_env), steps=35)
        edge_only_trajectory = run_episode(edge_only_env, edge_only, ExactOracle(edge_only_env), steps=35)

        contextual_final = contextual_trajectory.records[-1].deployment_gap
        edge_only_final = edge_only_trajectory.records[-1].deployment_gap
        self.assertLess(contextual_final, edge_only_final)


if __name__ == "__main__":
    unittest.main()
