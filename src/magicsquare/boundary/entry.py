"""Boundary entry point."""

from __future__ import annotations

from magicsquare.boundary.input_validator import InputValidator
from magicsquare.boundary.schemas import FailureResponse, SuccessResponse
from magicsquare.control.solve_partial_magic_square import SolvePartialMagicSquare


def resolve(grid: list[list[int]]) -> SuccessResponse | FailureResponse:
    """Delegate to Control use case after validation passes.

    Args:
        grid: Validated 4x4 grid.

    Returns:
        OK or ERROR envelope from Control layer.
    """
    return SolvePartialMagicSquare().execute(grid)


def validate_and_solve(
    grid: list[list[int]] | None,
) -> FailureResponse | SuccessResponse:
    """Validate grid input and solve when valid.

    Args:
        grid: Raw grid input, possibly ``None``.

    Returns:
        ERROR envelope on validation failure, otherwise resolver output.
    """
    failure = InputValidator().validate(grid)
    if failure is not None:
        return failure
    return resolve(grid)
