"""Boundary tests for AC-FR01-01 null grid rejection (UT-01).

AC-FR01-01 | Report/02 — ``grid=None`` must fail before Domain entry.
"""

from __future__ import annotations

from typing import Literal
from unittest.mock import MagicMock, patch

from pydantic import BaseModel

from magicsquare.boundary.entry import validate_and_solve

# AC-FR01-01 contract (Report/02 §2.2)
AC_FR01_01 = "AC-FR01-01"
PRD_SECTION = "Report/02"
EXPECTED_CODE = "ERR_NULL_GRID"
EXPECTED_MESSAGE = "Input grid is null."

EXECUTE_PATCH = (
    "magicsquare.control.solve_partial_magic_square.SolvePartialMagicSquare.execute"
)


class ErrorResponse(BaseModel):
    """ERROR envelope for Boundary failure responses."""

    status: Literal["ERROR"]
    code: str
    message: str


class TestAcFr0101NullGrid:
    """AC-FR01-01 | ERR_NULL_GRID — ``grid=None`` Track A (UT-01)."""

    def test_none_grid_returns_error_with_err_null_grid_code(self) -> None:
        """AC-FR01-01 | ERR_NULL_GRID — normal failure on null grid."""
        # AC-FR01-01
        # Given
        grid = None

        # When
        response = validate_and_solve(grid)

        # Then
        assert response["status"] == "ERROR"
        assert response["code"] == EXPECTED_CODE

    def test_none_grid_message_matches_report_02_exactly(self) -> None:
        """AC-FR01-01 | ERR_NULL_GRID — message byte-exact match."""
        # AC-FR01-01
        # Given
        grid = None

        # When
        response = validate_and_solve(grid)

        # Then
        assert response["message"] == EXPECTED_MESSAGE

    @patch(EXECUTE_PATCH)
    def test_none_grid_skips_execute_zero_calls_isolation(
        self, mock_execute: MagicMock
    ) -> None:
        """AC-FR01-01 | ERR_NULL_GRID — Control execute() not invoked."""
        # AC-FR01-01
        # Given
        grid = None

        # When
        validate_and_solve(grid)

        # Then
        mock_execute.assert_not_called()

    def test_none_grid_error_envelope_validates_with_pydantic(self) -> None:
        """AC-FR01-01 | ERR_NULL_GRID — ERROR envelope schema."""
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
        """AC-FR01-01 | ERR_NULL_GRID — explicit None null boundary."""
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
