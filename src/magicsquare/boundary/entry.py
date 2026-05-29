"""Boundary entry point."""

from __future__ import annotations

from magicsquare.boundary.input_validator import InputValidator
from magicsquare.boundary.schemas import FailureResponse, SuccessResponse
from magicsquare.entity.services.two_cell_solver import solution


def resolve(grid: list[list[int]]) -> SuccessResponse:
    """Delegate to Domain resolver after validation passes.

    Args:
        grid: Validated 4x4 grid.

    Returns:
        OK envelope with Domain ``int[6]`` result passthrough.
    """
    result = solution(grid)
    return SuccessResponse(status="OK", result=result)


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
