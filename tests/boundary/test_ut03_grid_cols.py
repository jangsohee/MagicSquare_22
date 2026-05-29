"""Boundary tests for AC-FR01-03 grid column count rejection (UT-03).

AC-FR01-03 | Report/02 ERR_GRID_COLS — any row length != 4 must fail before Domain entry.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from magicsquare.boundary.entry import validate_and_solve

# AC-FR01-03 contract (Report/02)
AC_FR01_03 = "AC-FR01-03"
EXPECTED_CODE = "ERR_GRID_COLS"
EXPECTED_MESSAGE = "Each row must have exactly 4 columns."


class TestUt03GridCols:
    """AC-FR01-03 | UT-03 — ERR_GRID_COLS on invalid column count."""

    def test_four_by_three_grid_returns_err_grid_cols(self) -> None:
        """AC-FR01-03 | 4×3 grid → ERR_GRID_COLS."""
        # AC-FR01-03
        # Given
        grid = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
            [10, 11, 12],
        ]

        # When
        response = validate_and_solve(grid)

        # Then
        assert response["status"] == "ERROR"
        assert response["code"] == EXPECTED_CODE
        assert response["message"] == EXPECTED_MESSAGE

    def test_four_empty_rows_returns_err_grid_cols(self) -> None:
        """AC-FR01-03 | [[]]*4 → ERR_GRID_COLS (row=4, col=0)."""
        # AC-FR01-03
        # Given
        grid = [[]] * 4

        # When
        response = validate_and_solve(grid)

        # Then
        assert response["status"] == "ERROR"
        assert response["code"] == EXPECTED_CODE
        assert response["message"] == EXPECTED_MESSAGE

    @patch("magicsquare.boundary.entry.resolve")
    def test_invalid_cols_skips_resolve_zero_calls_isolation(
        self, mock_resolve: MagicMock
    ) -> None:
        """AC-FR01-03 | ERR_GRID_COLS — Domain resolve() not invoked."""
        # AC-FR01-03
        # Given
        grid = [[]] * 4

        # When
        validate_and_solve(grid)

        # Then
        mock_resolve.assert_not_called()
