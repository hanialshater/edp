from __future__ import annotations

from math import sqrt
from random import Random
from typing import Protocol

from .math_utils import add_scaled, dot, identity, lcb, outer_add, quadratic_form_inverse, solve_linear_system
from .solver import solve_time_indexed_tsp
from .types import EdgeFeedback, TourAction, TourObservation


def _edge_key(left: int, right: int) -> tuple[int, int]:
    return (left, right) if left < right else (right, left)


class RouteAgent(Protocol):
    def plan(self, observation: TourObservation) -> TourAction:
        ...

    def deploy(self, observation: TourObservation) -> TourAction:
        ...

    def update(self, feedback: tuple[EdgeFeedback, ...]) -> None:
        ...


class ContextualLCBAgent:
    """Ridge-regression lower-confidence-bound agent for route-level feedback."""

    def __init__(
        self,
        feature_dim: int,
        start_node: int = 0,
        alpha: float = 0.85,
        ridge: float = 1.0,
        scouting_rounds: int = 3,
        seed: int = 0,
    ) -> None:
        self.feature_dim = feature_dim
        self.start_node = start_node
        self.alpha = alpha
        self.scouting_rounds = scouting_rounds
        self._rng = Random(seed)
        self._a = identity(feature_dim, ridge)
        self._b = [0.0 for _ in range(feature_dim)]
        self._round = 0

    def _theta(self) -> list[float]:
        return solve_linear_system(self._a, self._b)

    def _cost(self, observation: TourObservation, position: int, left: int, right: int, alpha: float) -> float:
        features = observation.edge_features[left][right][position]
        mean = dot(self._theta(), features)
        variance = quadratic_form_inverse(self._a, features)
        return max(0.01, lcb(mean, variance, alpha))

    def _scouting_tour(self, n_nodes: int) -> TourAction:
        rest = list(range(1, n_nodes))
        self._rng.shuffle(rest)
        return TourAction((self.start_node, *rest))

    def plan(self, observation: TourObservation) -> TourAction:
        if self._round < self.scouting_rounds:
            return self._scouting_tour(observation.n_nodes)
        return solve_time_indexed_tsp(
            observation.n_nodes,
            lambda position, left, right: self._cost(observation, position, left, right, self.alpha),
            start=self.start_node,
        )

    def deploy(self, observation: TourObservation) -> TourAction:
        return solve_time_indexed_tsp(
            observation.n_nodes,
            lambda position, left, right: self._cost(observation, position, left, right, 0.0),
            start=self.start_node,
        )

    def update(self, feedback: tuple[EdgeFeedback, ...]) -> None:
        for item in feedback:
            outer_add(self._a, item.features)
            add_scaled(self._b, item.features, item.observed_cost)
        self._round += 1


class EdgeOnlyLCBAgent:
    """Per-edge LCB baseline that deliberately ignores route-position context."""

    def __init__(
        self,
        start_node: int = 0,
        alpha: float = 0.85,
        prior_mean: float = 6.0,
        scouting_rounds: int = 3,
        seed: int = 0,
    ) -> None:
        self.start_node = start_node
        self.alpha = alpha
        self.prior_mean = prior_mean
        self.scouting_rounds = scouting_rounds
        self._rng = Random(seed)
        self._count: dict[tuple[int, int], int] = {}
        self._sum: dict[tuple[int, int], float] = {}
        self._round = 0

    def _scouting_tour(self, n_nodes: int) -> TourAction:
        rest = list(range(1, n_nodes))
        self._rng.shuffle(rest)
        return TourAction((self.start_node, *rest))

    def _edge_cost(self, left: int, right: int, alpha: float) -> float:
        edge = _edge_key(left, right)
        count = self._count.get(edge, 0)
        if count == 0:
            return max(0.01, self.prior_mean - alpha * 2.0)
        mean = self._sum[edge] / count
        return max(0.01, mean - alpha * 1.8 / sqrt(count))

    def plan(self, observation: TourObservation) -> TourAction:
        if self._round < self.scouting_rounds:
            return self._scouting_tour(observation.n_nodes)
        return solve_time_indexed_tsp(
            observation.n_nodes,
            lambda _position, left, right: self._edge_cost(left, right, self.alpha),
            start=self.start_node,
        )

    def deploy(self, observation: TourObservation) -> TourAction:
        return solve_time_indexed_tsp(
            observation.n_nodes,
            lambda _position, left, right: self._edge_cost(left, right, 0.0),
            start=self.start_node,
        )

    def update(self, feedback: tuple[EdgeFeedback, ...]) -> None:
        for item in feedback:
            edge = _edge_key(*item.edge)
            self._count[edge] = self._count.get(edge, 0) + 1
            self._sum[edge] = self._sum.get(edge, 0.0) + item.observed_cost
        self._round += 1


class RandomTourAgent:
    def __init__(self, start_node: int = 0, seed: int = 0) -> None:
        self.start_node = start_node
        self._rng = Random(seed)

    def _tour(self, n_nodes: int) -> TourAction:
        rest = [node for node in range(n_nodes) if node != self.start_node]
        self._rng.shuffle(rest)
        return TourAction((self.start_node, *rest))

    def plan(self, observation: TourObservation) -> TourAction:
        return self._tour(observation.n_nodes)

    def deploy(self, observation: TourObservation) -> TourAction:
        return self._tour(observation.n_nodes)

    def update(self, feedback: tuple[EdgeFeedback, ...]) -> None:
        del feedback
