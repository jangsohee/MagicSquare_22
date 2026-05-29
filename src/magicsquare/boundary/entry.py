"""Boundary entry point — delegates to ``UIBoundary`` (single facade)."""

from __future__ import annotations

from magicsquare.boundary.schemas import FailureResponse, SuccessResponse
from magicsquare.boundary.ui_boundary import UIBoundary


def validate_and_solve(
    grid: list[list[int]] | None,
) -> FailureResponse | SuccessResponse:
    """Validate grid input and solve when valid.

    Args:
        grid: Raw grid input, possibly ``None``.

    Returns:
        ERROR envelope on validation failure, otherwise solve result envelope.
    """
    return UIBoundary().solve(grid)
