"""Boundary tests for AC-FR01-05 empty cell count rejection (UT-06, UT-07).

AC-FR01-05 | Report/02 ERR_EMPTY_COUNT — zero count != 2 must fail before Domain entry.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from magicsquare.boundary.entry import validate_and_solve

# AC-FR01-05 contract (Report/02)
AC_FR01_05 = "AC-FR01-05"
EXPECTED_CODE = "ERR_EMPTY_COUNT"
EXPECTED_MESSAGE = "Grid must contain exactly 2 empty cells (value 0)."


class TestUt06EmptyCount:
    """AC-FR01-05 | UT-06/07 — ERR_EMPTY_COUNT on invalid zero count."""

    def test_one_empty_cell_returns_err_empty_count(self) -> None:
        """AC-FR01-05 | UT-06 — zero×1 → ERR_EMPTY_COUNT."""
        # AC-FR01-05
        # Given
        grid = [
            [16, 3, 2, 13],
            [5, 10, 11, 8],
            [9, 6, 7, 12],
            [4, 15, 14, 1],
        ]

        # When
        response = validate_and_solve(grid)

        # Then
        assert response["status"] == "ERROR"
        assert response["code"] == EXPECTED_CODE
        assert response["message"] == EXPECTED_MESSAGE

    def test_three_empty_cells_returns_err_empty_count(self) -> None:
        """AC-FR01-05 | UT-07 — zero×3 → ERR_EMPTY_COUNT."""
        # AC-FR01-05
        # Given
        grid = [
            [0, 3, 2, 13],
            [5, 0, 11, 8],
            [9, 6, 7, 12],
            [4, 15, 0, 1],
        ]

        # When
        response = validate_and_solve(grid)

        # Then
        assert response["status"] == "ERROR"
        assert response["code"] == EXPECTED_CODE
        assert response["message"] == EXPECTED_MESSAGE

    @patch("magicsquare.boundary.entry.resolve")
    def test_invalid_empty_count_skips_resolve_zero_calls_isolation(
        self, mock_resolve: MagicMock
    ) -> None:
        """AC-FR01-05 | ERR_EMPTY_COUNT — Domain resolve() not invoked."""
        # AC-FR01-05
        # Given
        grid = [
            [0, 3, 2, 13],
            [5, 0, 11, 8],
            [9, 6, 7, 12],
            [4, 15, 0, 1],
        ]

        # When
        validate_and_solve(grid)

        # Then
        mock_resolve.assert_not_called()
