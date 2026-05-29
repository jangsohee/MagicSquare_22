"""Direct ``UIBoundary`` tests (Report/16 — U-OUT · U-FLOW · UT-09)."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from magicsquare.boundary.example_grids import UT09_PARTIAL_GRID, UT09_PARTIAL_RESULT
from magicsquare.boundary.schemas import (
    ERR_NULL_GRID_CODE,
    ERR_NULL_GRID_MESSAGE,
    ERR_VALUE_RANGE_CODE,
)
from magicsquare.boundary.ui_boundary import UIBoundary

EXECUTE_PATCH = (
    "magicsquare.control.solve_partial_magic_square.SolvePartialMagicSquare.execute"
)

# U-OUT G1 partial grid
G1_PARTIAL: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]
G1_EXPECTED_RESULT = [2, 2, 10, 3, 3, 7]

# U-FLOW-02 E004
E004_GRID: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 17],
]


class TestUiBoundarySolve:
    """``UIBoundary.solve`` — contract without ``entry`` facade."""

    def test_ut09_valid_grid_returns_ok_envelope(self) -> None:
        """UT-09 | valid grid → OK + exact ``int[6]``."""
        boundary = UIBoundary()
        grid = [row[:] for row in UT09_PARTIAL_GRID]

        response = boundary.solve(grid)

        assert response["status"] == "OK"
        assert response["result"] == UT09_PARTIAL_RESULT

    def test_null_grid_returns_err_null_grid(self) -> None:
        """UT-01 | ``None`` → ERR_NULL_GRID before Control."""
        boundary = UIBoundary()

        response = boundary.solve(None)

        assert response["status"] == "ERROR"
        assert response["code"] == ERR_NULL_GRID_CODE
        assert response["message"] == ERR_NULL_GRID_MESSAGE

    @patch(EXECUTE_PATCH)
    def test_invalid_grid_skips_execute_zero_calls(
        self, mock_execute: MagicMock
    ) -> None:
        """U-FLOW-02 | E004 → execute not invoked."""
        boundary = UIBoundary()
        grid = [row[:] for row in E004_GRID]

        response = boundary.solve(grid)

        assert response["status"] == "ERROR"
        assert response["code"] == ERR_VALUE_RANGE_CODE
        mock_execute.assert_not_called()

    def test_u_out_g1_six_element_one_indexed_result(self) -> None:
        """U-OUT-01/02 | G1 → len 6, coords 1-index."""
        boundary = UIBoundary()
        grid = [row[:] for row in G1_PARTIAL]

        response = boundary.solve(grid)

        assert response["status"] == "OK"
        result = response["result"]
        assert len(result) == 6
        assert all(1 <= result[i] <= 4 for i in (0, 1, 3, 4))
        assert result == G1_EXPECTED_RESULT
