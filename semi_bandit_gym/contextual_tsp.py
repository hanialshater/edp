from __future__ import annotations

from dataclasses import dataclass
from math import exp, hypot
from random import Random

from .solver import action_edges, solve_time_indexed_tsp
from .types import EdgeFeedback, Evaluation, StepResult, TourAction, TourObservation


def _canonical_edge(left: int, right: int) -> tuple[int, int]:
    return (left, right) if left < right else (right, left)


@dataclass(frozen=True)
class ContextualTSPConfig:
    n_nodes: int = 8
    horizon: int = 60
    noise_std: float = 0.08
    start_node: int = 0
    fixed_day_context: bool = True


class ContextualTSPEnv:
    """Small exact route-level contextual semi-bandit environment.

    The world has a fixed hidden expected-cost law. There is *no per-day drift*:
    repeated execution changes only observation noise. The public context includes
    edge and position features; the hidden coefficients remain private.

    ``step`` reveals feedback only for selected route edges, one labelled record per
    edge. The direct result intentionally excludes the hidden world and oracle.
    """

    feature_names = (
        "bias",
        "distance",
        "centrality",
        "rush",
        "centrality_x_rush",
        "distance_x_rush",
    )

    def __init__(self, config: ContextualTSPConfig | None = None, seed: int = 0) -> None:
        self.config = config or ContextualTSPConfig()
        if not 4 <= self.config.n_nodes <= 12:
            raise ValueError("n_nodes must be between 4 and 12 for exact tiny-gym use.")
        self._seed = seed
        self._rng = Random(seed)
        self._build_world()
        self._day = 0
        self._last_action: TourAction | None = None

    def _build_world(self) -> None:
        n_nodes = self.config.n_nodes
        self._coordinates = tuple(
            (self._rng.uniform(0.0, 1.0), self._rng.uniform(0.0, 1.0))
            for _ in range(n_nodes)
        )
        centroid_x = sum(point[0] for point in self._coordinates) / n_nodes
        centroid_y = sum(point[1] for point in self._coordinates) / n_nodes
        maximum_radius = max(
            hypot(point[0] - centroid_x, point[1] - centroid_y)
            for point in self._coordinates
        )
        self._centrality = tuple(
            max(0.0, 1.0 - hypot(point[0] - centroid_x, point[1] - centroid_y) / maximum_radius)
            for point in self._coordinates
        )

        self._base_edge: dict[tuple[int, int], float] = {}
        self._hidden_edge_residual: dict[tuple[int, int], float] = {}
        for left in range(n_nodes):
            for right in range(left + 1, n_nodes):
                raw_distance = hypot(
                    self._coordinates[left][0] - self._coordinates[right][0],
                    self._coordinates[left][1] - self._coordinates[right][1],
                )
                self._base_edge[(left, right)] = 1.0 + 5.0 * raw_distance
                self._hidden_edge_residual[(left, right)] = self._rng.uniform(-0.12, 0.12)

        # Fixed, hidden contextual law. The public feature map is known; coefficients are not.
        # The strong centrality x rush interaction makes the benchmark diagnose whether a
        # policy can generalize across edge features and route position.
        self._theta = (0.80, 1.15, 0.10, 1.80, 4.20, 0.35)
        self._day_context = {"weather": 0.0, "start_minute": 480.0}

    @property
    def n_nodes(self) -> int:
        return self.config.n_nodes

    @property
    def feature_dim(self) -> int:
        return len(self.feature_names)

    def reset(self, seed: int | None = None) -> TourObservation:
        if seed is not None:
            self._seed = seed
            self._rng = Random(seed)
            self._build_world()
        self._day = 0
        self._last_action = None
        return self._observation()

    def _observation(self) -> TourObservation:
        n_nodes = self.n_nodes
        feature_tensor = tuple(
            tuple(
                tuple(
                    (
                        tuple(0.0 for _ in self.feature_names)
                        if left == right
                        else self.public_edge_features(left, right, position)
                    )
                    for position in range(n_nodes)
                )
                for right in range(n_nodes)
            )
            for left in range(n_nodes)
        )
        return TourObservation(
            day=self._day,
            n_nodes=n_nodes,
            horizon=self.config.horizon,
            exogenous_context=dict(self._day_context),
            edge_features=feature_tensor,
        )

    def public_edge_features(self, left: int, right: int, position: int) -> tuple[float, ...]:
        """Known feature map; it contains no hidden expected cost or coefficient."""

        if left == right:
            raise ValueError("Self-loops are not valid route edges.")
        if not 0 <= position < self.n_nodes:
            raise ValueError("route position must be within the tour.")

        edge = _canonical_edge(left, right)
        distance = min(1.0, (self._base_edge[edge] - 1.0) / 5.0)
        centrality = (self._centrality[left] + self._centrality[right]) / 2.0
        normalized_position = position / max(1, self.n_nodes - 1)
        rush = exp(-((normalized_position - 0.52) / 0.22) ** 2)
        return (
            1.0,
            distance,
            centrality,
            rush,
            centrality * rush,
            distance * rush,
        )

    def _hidden_expected_cost(self, left: int, right: int, position: int) -> float:
        edge = _canonical_edge(left, right)
        features = self.public_edge_features(left, right, position)
        contextual = sum(weight * value for weight, value in zip(self._theta, features, strict=True))
        return max(0.05, self._base_edge[edge] + contextual + self._hidden_edge_residual[edge])

    def _validate(self, action: TourAction) -> None:
        expected = tuple(range(self.n_nodes))
        if len(action.tour) != self.n_nodes:
            raise ValueError(f"Expected {self.n_nodes} visited nodes, received {len(action.tour)}.")
        if tuple(sorted(action.tour)) != expected:
            raise ValueError("Action must visit every node exactly once.")
        if action.tour[0] != self.config.start_node:
            raise ValueError(f"Tour must start at node {self.config.start_node}.")

    def step(self, action: TourAction) -> StepResult:
        self._validate(action)
        feedback: list[EdgeFeedback] = []
        total_cost = 0.0

        for position, left, right in action_edges(action):
            expected_cost = self._hidden_expected_cost(left, right, position)
            observed_cost = max(0.01, expected_cost + self._rng.gauss(0.0, self.config.noise_std))
            total_cost += observed_cost
            feedback.append(
                EdgeFeedback(
                    edge=_canonical_edge(left, right),
                    route_position=position,
                    features=self.public_edge_features(left, right, position),
                    observed_cost=observed_cost,
                )
            )

        self._day += 1
        self._last_action = action
        terminated = self._day >= self.config.horizon
        return StepResult(
            observation=self._observation(),
            feedback=tuple(feedback),
            route_cost=total_cost,
            terminated=terminated,
            truncated=False,
            info={"day": float(self._day), "n_feedback": float(len(feedback))},
        )

    # Evaluator-only hooks. Keep private by convention and do not pass env to an agent.
    def _expected_action_cost(self, action: TourAction) -> float:
        self._validate(action)
        return sum(
            self._hidden_expected_cost(left, right, position)
            for position, left, right in action_edges(action)
        )

    def _oracle_action(self) -> TourAction:
        return solve_time_indexed_tsp(
            self.n_nodes,
            lambda position, left, right: self._hidden_expected_cost(left, right, position),
            start=self.config.start_node,
        )


class ExactOracle:
    """Evaluator-only access to the hidden expected-cost world."""

    def __init__(self, env: ContextualTSPEnv) -> None:
        self._env = env
        self._oracle_action = env._oracle_action()
        self._oracle_cost = env._expected_action_cost(self._oracle_action)

    @property
    def action(self) -> TourAction:
        return self._oracle_action

    @property
    def cost(self) -> float:
        return self._oracle_cost

    def evaluate(self, action: TourAction) -> Evaluation:
        expected_cost = self._env._expected_action_cost(action)
        return Evaluation(
            expected_cost=expected_cost,
            oracle_cost=self._oracle_cost,
            gap_to_oracle=expected_cost - self._oracle_cost,
        )
