"""Boundary tests for AC-FR01-02 grid row count rejection (UT-02).

AC-FR01-02 | Report/02 ERR_GRID_ROWS — row count != 4 must fail before Domain entry.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from magicsquare.boundary.entry import validate_and_solve

# AC-FR01-02 contract (Report/02)
AC_FR01_02 = "AC-FR01-02"
EXPECTED_CODE = "ERR_GRID_ROWS"
EXPECTED_MESSAGE = "Grid must have exactly 4 rows."


class TestUt02GridRows:
    """AC-FR01-02 | UT-02 — ERR_GRID_ROWS on invalid row count."""

    def test_empty_grid_returns_err_grid_rows(self) -> None:
        """AC-FR01-02 | grid=[] → ERR_GRID_ROWS."""
        # AC-FR01-02
        # Given
        grid: list[list[int]] = []

        # When
        response = validate_and_solve(grid)

        # Then
        assert response["status"] == "ERROR"
        assert response["code"] == EXPECTED_CODE
        assert response["message"] == EXPECTED_MESSAGE

    def test_three_by_four_grid_returns_err_grid_rows(self) -> None:
        """AC-FR01-02 | 3×4 grid → ERR_GRID_ROWS."""
        # AC-FR01-02
        # Given
        grid = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
        ]

        # When
        response = validate_and_solve(grid)

        # Then
        assert response["status"] == "ERROR"
        assert response["code"] == EXPECTED_CODE
        assert response["message"] == EXPECTED_MESSAGE

    def test_five_by_five_grid_returns_err_grid_rows(self) -> None:
        """AC-FR01-02 | 5×5 grid → ERR_GRID_ROWS."""
        # AC-FR01-02
        # Given
        grid = [
            [1, 2, 3, 4, 5],
            [6, 7, 8, 9, 10],
            [11, 12, 13, 14, 15],
            [16, 1, 2, 3, 4],
            [5, 6, 7, 8, 9],
        ]

        # When
        response = validate_and_solve(grid)

        # Then
        assert response["status"] == "ERROR"
        assert response["code"] == EXPECTED_CODE
        assert response["message"] == EXPECTED_MESSAGE

    @patch("magicsquare.boundary.entry.resolve")
    def test_invalid_rows_skips_resolve_zero_calls_isolation(
        self, mock_resolve: MagicMock
    ) -> None:
        """AC-FR01-02 | ERR_GRID_ROWS — Domain resolve() not invoked."""
        # AC-FR01-02
        # Given
        grid: list[list[int]] = []

        # When
        validate_and_solve(grid)

        # Then
        mock_resolve.assert_not_called()
