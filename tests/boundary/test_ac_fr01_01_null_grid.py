"""Boundary RED tests for AC-FR01-01 null grid rejection (UT-01).

AC-FR01-01 | PRD §8.1 INVALID_SIZE — ``grid=None`` must fail before Domain entry.
"""

from __future__ import annotations

from typing import Literal
from unittest.mock import MagicMock, patch

from pydantic import BaseModel

from magicsquare.boundary.entry import validate_and_solve

# AC-FR01-01 contract (PRD §8.1)
AC_FR01_01 = "AC-FR01-01"
PRD_SECTION = "PRD §8.1"
EXPECTED_CODE = "INVALID_SIZE"
EXPECTED_MESSAGE = "Grid must be 4x4."


class ErrorResponse(BaseModel):
    """ERROR envelope for Boundary failure responses."""

    status: Literal["ERROR"]
    code: str
    message: str


class TestAcFr0101NullGrid:
    """AC-FR01-01 | PRD §8.1 INVALID_SIZE — ``grid=None`` Track A RED (UT-01)."""

    def test_none_grid_returns_error_with_invalid_size_code(self) -> None:
        """AC-FR01-01 | PRD §8.1 INVALID_SIZE — normal failure on null grid."""
        # AC-FR01-01
        # Given
        grid = None

        # When
        response = validate_and_solve(grid)

        # Then
        assert response["status"] == "ERROR"
        assert response["code"] == EXPECTED_CODE

    def test_none_grid_message_matches_prd_section_8_1_exactly(self) -> None:
        """AC-FR01-01 | PRD §8.1 INVALID_SIZE — message byte-exact match."""
        # AC-FR01-01
        # Given
        grid = None

        # When
        response = validate_and_solve(grid)

        # Then
        assert response["message"] == EXPECTED_MESSAGE

    @patch("magicsquare.boundary.entry.resolve")
    def test_none_grid_skips_resolve_zero_calls_isolation(
        self, mock_resolve: MagicMock
    ) -> None:
        """AC-FR01-01 | PRD §8.1 INVALID_SIZE — Domain resolve() not invoked."""
        # AC-FR01-01
        # Given
        grid = None

        # When
        validate_and_solve(grid)

        # Then
        mock_resolve.assert_not_called()

    def test_none_grid_error_envelope_validates_with_pydantic(self) -> None:
        """AC-FR01-01 | PRD §8.1 INVALID_SIZE — ERROR envelope schema."""
        # AC-FR01-01
        # Given
        grid = None

        # When
        response = validate_and_solve(grid)

        # Then
        parsed = ErrorResponse.model_validate(response)
        assert parsed.code == EXPECTED_CODE
        assert parsed.message == EXPECTED_MESSAGE

    def test_none_grid_explicit_none_null_boundary_rejection(self) -> None:
        """AC-FR01-01 | PRD §8.1 INVALID_SIZE — explicit None null boundary."""
        # AC-FR01-01
        # Given — null boundary: only ``None`` satisfies ``grid is None``
        grid: list[list[int]] | None = None
        assert grid is None

        # When
        response = validate_and_solve(grid)

        # Then — failure path only; no success ``result`` field (AC-FR01-02~05 out of scope)
        assert response["status"] == "ERROR"
        assert response["code"] == EXPECTED_CODE
        assert response["message"] == EXPECTED_MESSAGE
        assert "result" not in response
