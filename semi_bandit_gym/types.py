from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence


Edge = tuple[int, int]


@dataclass(frozen=True)
class TourAction:
    """A Hamiltonian cycle represented by its ordered vertex visits.

    The closing edge from the final vertex back to the first is implicit.
    """

    tour: tuple[int, ...]

    @classmethod
    def from_sequence(cls, tour: Sequence[int]) -> "TourAction":
        return cls(tuple(int(node) for node in tour))


@dataclass(frozen=True)
class TourObservation:
    """Public information available before choosing the next whole route."""

    day: int
    n_nodes: int
    horizon: int
    exogenous_context: Mapping[str, float]
    edge_features: tuple[tuple[tuple[tuple[float, ...], ...], ...], ...]


@dataclass(frozen=True)
class EdgeFeedback:
    """One labelled component-level observation from the selected tour."""

    edge: Edge
    route_position: int
    features: tuple[float, ...]
    observed_cost: float


@dataclass(frozen=True)
class StepResult:
    """Feedback returned by a route-level semi-bandit environment."""

    observation: TourObservation
    feedback: tuple[EdgeFeedback, ...]
    route_cost: float
    terminated: bool
    truncated: bool
    info: Mapping[str, float]


@dataclass(frozen=True)
class Evaluation:
    """Evaluator-only metrics. Never pass this object to an agent."""

    expected_cost: float
    oracle_cost: float
    gap_to_oracle: float


@dataclass(frozen=True)
class StepRecord:
    day: int
    exploration_expected_cost: float
    deployment_expected_cost: float
    oracle_cost: float
    deployment_gap: float
    observed_route_cost: float


@dataclass(frozen=True)
class Trajectory:
    records: tuple[StepRecord, ...]
