"""Boundary tests for AC-FR01-04 value range rejection (UT-04, UT-05).

AC-FR01-04 | Report/02 ERR_VALUE_RANGE — cell ∉ {0}∪[1,16] must fail before Domain entry.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from magicsquare.boundary.entry import validate_and_solve

EXECUTE_PATCH = (
    "magicsquare.control.solve_partial_magic_square.SolvePartialMagicSquare.execute"
)

# AC-FR01-04 contract (Report/02)
AC_FR01_04 = "AC-FR01-04"
EXPECTED_CODE = "ERR_VALUE_RANGE"
EXPECTED_MESSAGE = "Cell value must be 0 or between 1 and 16 inclusive."


class TestUIn04ValueRange:
    """AC-FR01-04 | UT-04/05 — ERR_VALUE_RANGE on invalid cell values."""

    def test_cell_17_returns_err_value_range(self) -> None:
        """AC-FR01-04 | UT-04 — cell=17 → ERR_VALUE_RANGE."""
        # AC-FR01-04
        # Given
        grid = [
            [16, 3, 2, 13],
            [5, 10, 11, 8],
            [9, 6, 7, 12],
            [4, 15, 14, 17],
        ]

        # When
        response = validate_and_solve(grid)

        # Then
        assert response["status"] == "ERROR"
        assert response["code"] == EXPECTED_CODE
        assert response["message"] == EXPECTED_MESSAGE

    def test_cell_minus_one_returns_err_value_range(self) -> None:
        """AC-FR01-04 | UT-05 — cell=-1 → ERR_VALUE_RANGE."""
        # AC-FR01-04
        # Given
        grid = [
            [16, 3, 2, 13],
            [5, -1, 11, 8],
            [9, 6, 7, 12],
            [4, 15, 14, 1],
        ]

        # When
        response = validate_and_solve(grid)

        # Then
        assert response["status"] == "ERROR"
        assert response["code"] == EXPECTED_CODE
        assert response["message"] == EXPECTED_MESSAGE

    @patch(EXECUTE_PATCH)
    def test_invalid_range_skips_execute_zero_calls_isolation(
        self, mock_execute: MagicMock
    ) -> None:
        """AC-FR01-04 | ERR_VALUE_RANGE — Control execute() not invoked."""
        # AC-FR01-04
        # Given
        grid = [
            [16, 3, 2, 13],
            [5, 10, 11, 8],
            [9, 6, 7, 12],
            [4, 15, 14, 17],
        ]

        # When
        validate_and_solve(grid)

        # Then
        mock_execute.assert_not_called()
