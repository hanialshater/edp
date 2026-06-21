from __future__ import annotations

from math import sqrt
from typing import Sequence


def zeros(rows: int, cols: int) -> list[list[float]]:
    return [[0.0 for _ in range(cols)] for _ in range(rows)]


def identity(size: int, scale: float = 1.0) -> list[list[float]]:
    matrix = zeros(size, size)
    for index in range(size):
        matrix[index][index] = scale
    return matrix


def dot(left: Sequence[float], right: Sequence[float]) -> float:
    return sum(a * b for a, b in zip(left, right, strict=True))


def outer_add(matrix: list[list[float]], vector: Sequence[float]) -> None:
    for row, value_i in enumerate(vector):
        for col, value_j in enumerate(vector):
            matrix[row][col] += value_i * value_j


def add_scaled(target: list[float], vector: Sequence[float], scale: float) -> None:
    for index, value in enumerate(vector):
        target[index] += scale * value


def solve_linear_system(matrix: Sequence[Sequence[float]], target: Sequence[float]) -> list[float]:
    """Gaussian elimination with partial pivoting for tiny dense systems."""

    n = len(target)
    augmented = [list(matrix[row]) + [float(target[row])] for row in range(n)]

    for column in range(n):
        pivot = max(range(column, n), key=lambda row: abs(augmented[row][column]))
        if abs(augmented[pivot][column]) < 1e-12:
            raise ValueError("Singular system.")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]

        pivot_value = augmented[column][column]
        for index in range(column, n + 1):
            augmented[column][index] /= pivot_value

        for row in range(n):
            if row == column:
                continue
            factor = augmented[row][column]
            if factor == 0.0:
                continue
            for index in range(column, n + 1):
                augmented[row][index] -= factor * augmented[column][index]

    return [augmented[row][n] for row in range(n)]


def quadratic_form_inverse(matrix: Sequence[Sequence[float]], vector: Sequence[float]) -> float:
    solution = solve_linear_system(matrix, vector)
    return max(0.0, dot(vector, solution))


def lcb(mean: float, variance: float, alpha: float) -> float:
    return mean - alpha * sqrt(max(variance, 0.0))
