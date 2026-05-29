"""Boundary tests for UT-09 valid solve success envelope (AC-FR01-07).

Report/02 UT-09 — valid partial grid → status OK, result exact match, Domain 1 call.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from magicsquare.boundary.entry import validate_and_solve

EXECUTE_PATCH = (
    "magicsquare.control.solve_partial_magic_square.SolvePartialMagicSquare.execute"
)

# UT-09 / DT-03 contract (Report/02)
UT09_GRID: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 0],
]
# B-03 reverse assignment for UT-09/DT-03 (forward [3,3,1,4,4,7] is not magic).
EXPECTED_RESULT = [3, 3, 7, 4, 4, 1]


class TestUt09ValidSolve:
    """AC-FR01-07 | UT-09 — OK envelope on valid partial grid."""

    def test_valid_grid_returns_ok_with_exact_result(self) -> None:
        """UT-09 | valid grid → status OK, result [3,3,7,4,4,1]."""
        # UT-09
        # Given
        grid = [row[:] for row in UT09_GRID]

        # When
        response = validate_and_solve(grid)

        # Then
        assert response["status"] == "OK"
        assert response["result"] == EXPECTED_RESULT

    @patch(EXECUTE_PATCH)
    def test_valid_grid_calls_execute_exactly_once(
        self, mock_execute: MagicMock
    ) -> None:
        """UT-09 | valid grid → Control execute() invoked exactly once."""
        # UT-09
        # Given
        mock_execute.return_value = EXPECTED_RESULT
        grid = [row[:] for row in UT09_GRID]

        # When
        validate_and_solve(grid)

        # Then
        mock_execute.assert_called_once()
