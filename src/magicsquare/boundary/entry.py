"""Boundary entry point — delegates to ``UIBoundary`` (single facade)."""

from __future__ import annotations

from magicsquare.boundary.schemas import FailureResponse, SuccessResponse
from magicsquare.boundary.ui_boundary import UIBoundary

# Module-level facade (validator/use-case injected once per process).
_DEFAULT_BOUNDARY = UIBoundary()


def validate_and_solve(
    grid: list[list[int]] | None,
    boundary: UIBoundary | None = None,
) -> FailureResponse | SuccessResponse:
    """Validate grid input and solve when valid.

    Args:
        grid: Raw grid input, possibly ``None``.
        boundary: Optional ``UIBoundary`` override (tests).

    Returns:
        ERROR envelope on validation failure, otherwise solve result envelope.
    """
    target = boundary if boundary is not None else _DEFAULT_BOUNDARY
    return target.solve(grid)
