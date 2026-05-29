"""Integration tests for IT-FAIL invalid input E2E paths.

Real Boundary + Control + Entity — Domain Mock forbidden (Report/02 REG-06).
"""

from __future__ import annotations

from magicsquare.boundary.schemas import (
    ERR_DUPLICATE_CODE,
    ERR_EMPTY_COUNT_CODE,
    ERR_EMPTY_COUNT_MESSAGE,
    ERR_NO_SOLUTION_CODE,
    ERR_NO_SOLUTION_MESSAGE,
)
from magicsquare.boundary.ui_boundary import UIBoundary

# IT-FAIL-01 — three empty cells (UT-07)
IT_FAIL_01_GRID: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 0, 0],
]

# IT-FAIL-02 — DT-10 / G3 unsolvable (D-SOL-03)
IT_FAIL_02_GRID: list[list[int]] = [
    [16, 0, 2, 13],
    [5, 10, 0, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 3],
]

# IT-FAIL-04 — duplicate non-zero (UT-08)
IT_FAIL_04_GRID: list[list[int]] = [
    [16, 3, 2, 0],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 5, 0],
]


class TestItFailValidation:
    """IT-FAIL-01/02/04 — invalid E2E without Domain Mock."""

    def test_it_fail_01_three_empty_cells_returns_err_empty_count(self) -> None:
        """IT-FAIL-01 | zero×3 → ERROR / ERR_EMPTY_COUNT."""
        # IT-FAIL-01
        # Given
        boundary = UIBoundary()
        grid = [row[:] for row in IT_FAIL_01_GRID]

        # When
        response = boundary.solve(grid)

        # Then
        assert response["status"] == "ERROR"
        assert response["code"] == ERR_EMPTY_COUNT_CODE
        assert response["message"] == ERR_EMPTY_COUNT_MESSAGE

    def test_it_fail_02_unsolvable_grid_returns_err_no_solution(self) -> None:
        """IT-FAIL-02 | DT-10 → ERROR / ERR_NO_SOLUTION."""
        # IT-FAIL-02
        # Given
        boundary = UIBoundary()
        grid = [row[:] for row in IT_FAIL_02_GRID]

        # When
        response = boundary.solve(grid)

        # Then
        assert response["status"] == "ERROR"
        assert response["code"] == ERR_NO_SOLUTION_CODE
        assert response["message"] == ERR_NO_SOLUTION_MESSAGE

    def test_it_fail_04_duplicate_returns_err_duplicate(self) -> None:
        """IT-FAIL-04 | duplicate → ERROR / ERR_DUPLICATE."""
        # IT-FAIL-04
        # Given
        boundary = UIBoundary()
        grid = [row[:] for row in IT_FAIL_04_GRID]

        # When
        response = boundary.solve(grid)

        # Then
        assert response["status"] == "ERROR"
        assert response["code"] == ERR_DUPLICATE_CODE
        assert response["message"] == "Duplicate non-zero value: 5."
