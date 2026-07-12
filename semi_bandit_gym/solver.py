from __future__ import annotations

from collections.abc import Callable
from itertools import permutations
from math import inf

from .types import TourAction


TimeIndexedCost = Callable[[int, int, int], float]


def solve_time_indexed_tsp(n_nodes: int, cost: TimeIndexedCost, start: int = 0) -> TourAction:
    """Solve a small time-indexed TSP exactly by Held-Karp dynamic programming.

    ``cost(position, from_node, to_node)`` may depend on route position. This makes
    route position a first-class, action-derived context rather than an afterthought.

    The result is exact for this finite action space and is intended for tiny
    correctness environments (roughly 6-12 nodes), not Berlin52-scale rendering.
    """

    if n_nodes < 3:
        raise ValueError("A tour needs at least three nodes.")
    if not 0 <= start < n_nodes:
        raise ValueError("start must be a valid node index.")

    others = [node for node in range(n_nodes) if node != start]
    start_mask = 1 << start
    dp: dict[tuple[int, int], tuple[float, tuple[int, ...]]] = {
        (start_mask, start): (0.0, (start,)),
    }

    for visited_count in range(1, n_nodes):
        next_dp: dict[tuple[int, int], tuple[float, tuple[int, ...]]] = {}
        for (mask, last), (path_cost, path) in dp.items():
            if mask.bit_count() != visited_count:
                continue
            position = visited_count - 1
            for candidate in others:
                bit = 1 << candidate
                if mask & bit:
                    continue
                next_mask = mask | bit
                candidate_cost = path_cost + cost(position, last, candidate)
                key = (next_mask, candidate)
                previous = next_dp.get(key)
                if previous is None or candidate_cost < previous[0]:
                    next_dp[key] = (candidate_cost, path + (candidate,))
        dp = next_dp

    full_mask = (1 << n_nodes) - 1
    best_cost = inf
    best_path: tuple[int, ...] | None = None
    closing_position = n_nodes - 1
    for (mask, last), (path_cost, path) in dp.items():
        if mask != full_mask:
            continue
        candidate_cost = path_cost + cost(closing_position, last, start)
        if candidate_cost < best_cost:
            best_cost = candidate_cost
            best_path = path

    if best_path is None:
        raise RuntimeError("No feasible Hamiltonian cycle found.")
    return TourAction(best_path)


def brute_force_time_indexed_tsp(n_nodes: int, cost: TimeIndexedCost, start: int = 0) -> TourAction:
    """Slow reference solver used only in tests to verify Held-Karp correctness."""

    best_cost = inf
    best_tour: tuple[int, ...] | None = None
    others = [node for node in range(n_nodes) if node != start]
    for rest in permutations(others):
        tour = (start,) + rest
        total = 0.0
        for position in range(n_nodes):
            total += cost(position, tour[position], tour[(position + 1) % n_nodes])
        if total < best_cost:
            best_cost = total
            best_tour = tour

    if best_tour is None:
        raise RuntimeError("No feasible Hamiltonian cycle found.")
    return TourAction(best_tour)


def action_edges(action: TourAction) -> tuple[tuple[int, int, int], ...]:
    """Return (position, from_node, to_node) for every selected edge."""

    n_nodes = len(action.tour)
    return tuple(
        (position, action.tour[position], action.tour[(position + 1) % n_nodes])
        for position in range(n_nodes)
    )
