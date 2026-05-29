"""Boundary tests for AC-FR01-06 duplicate non-zero rejection (UT-08).

AC-FR01-06 | Report/02 ERR_DUPLICATE — non-zero duplicate must fail before Domain entry.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from magicsquare.boundary.entry import validate_and_solve

# AC-FR01-06 contract (Report/02)
AC_FR01_06 = "AC-FR01-06"
EXPECTED_CODE = "ERR_DUPLICATE"
EXPECTED_MESSAGE = "Duplicate non-zero value: 5."


class TestUIn05Duplicate:
    """AC-FR01-06 | UT-08 — ERR_DUPLICATE on non-zero duplicate."""

    def test_duplicate_five_returns_err_duplicate(self) -> None:
        """AC-FR01-06 | UT-08 — two 5s → ERR_DUPLICATE."""
        # AC-FR01-06
        # Given
        grid = [
            [16, 3, 2, 0],
            [5, 10, 11, 8],
            [9, 6, 7, 12],
            [4, 15, 5, 0],
        ]

        # When
        response = validate_and_solve(grid)

        # Then
        assert response["status"] == "ERROR"
        assert response["code"] == EXPECTED_CODE
        assert response["message"] == EXPECTED_MESSAGE

    @patch("magicsquare.boundary.entry.resolve")
    def test_duplicate_skips_resolve_zero_calls_isolation(
        self, mock_resolve: MagicMock
    ) -> None:
        """AC-FR01-06 | ERR_DUPLICATE — Domain resolve() not invoked."""
        # AC-FR01-06
        # Given
        grid = [
            [16, 3, 2, 0],
            [5, 10, 11, 8],
            [9, 6, 7, 12],
            [4, 15, 5, 0],
        ]

        # When
        validate_and_solve(grid)

        # Then
        mock_resolve.assert_not_called()
