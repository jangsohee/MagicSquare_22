"""Integration tests for IT-OK solve E2E paths.

Real Boundary + Control + Entity (+ Data for IT-OK-02) — Domain Mock forbidden.
"""

from __future__ import annotations

from magicsquare.boundary.ui_boundary import UIBoundary
from magicsquare.control.solve_magic_square_use_case import SolveMagicSquareUseCase
from magicsquare.data.in_memory_matrix_repository import InMemoryMatrixRepository

# IT-OK-01 / UT-09 / DT-03
IT_OK_01_GRID: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 0],
]
IT_OK_01_RESULT = [3, 3, 7, 4, 4, 1]

# IT-OK-03 / DT-06 / G2 reverse assignment
IT_OK_03_GRID: list[list[int]] = [
    [0, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 0],
]
IT_OK_03_RESULT = [1, 1, 16, 4, 4, 1]


class TestItOkSolve:
    """IT-OK-01~03 — end-to-end solve without Domain Mock."""

    def test_it_ok_01_ut09_grid_returns_ok_with_exact_result(self) -> None:
        """IT-OK-01 | UT-09 Given → status OK, result passthrough."""
        # IT-OK-01
        # Given
        boundary = UIBoundary()
        grid = [row[:] for row in IT_OK_01_GRID]

        # When
        response = boundary.solve(grid)

        # Then
        assert response["status"] == "OK"
        assert response["result"] == IT_OK_01_RESULT

    def test_it_ok_02_save_and_load_round_trip(self) -> None:
        """IT-OK-02 | solve + session1 → loadGrid/loadResult round-trip."""
        # IT-OK-02
        # Given
        repository = InMemoryMatrixRepository()
        use_case = SolveMagicSquareUseCase(repository)
        grid = [row[:] for row in IT_OK_01_GRID]
        session_id = "session1"

        # When
        response = use_case.execute(grid, session_id)

        # Then
        assert response["status"] == "OK"
        assert repository.load_grid(session_id) == grid
        assert repository.load_result(session_id) == response["result"]

    def test_it_ok_03_dt06_reverse_path_returns_expected_result(self) -> None:
        """IT-OK-03 | DT-06 → status OK, reverse assignment result."""
        # IT-OK-03
        # Given
        boundary = UIBoundary()
        grid = [row[:] for row in IT_OK_03_GRID]

        # When
        response = boundary.solve(grid)

        # Then
        assert response["status"] == "OK"
        assert response["result"] == IT_OK_03_RESULT
