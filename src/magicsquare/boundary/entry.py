"""Boundary entry point."""

from __future__ import annotations

from typing import Any

from magicsquare.boundary.input_validator import InputValidator
from magicsquare.boundary.schemas import FailureResponse


def resolve(grid: list[list[int]]) -> dict[str, Any]:
    """Delegate to Domain resolver after validation passes.

    Args:
        grid: Validated 4x4 grid.

    Raises:
        NotImplementedError: Domain resolver is not implemented yet.
    """
    raise NotImplementedError("Domain resolve is not implemented.")


def validate_and_solve(
    grid: list[list[int]] | None,
) -> FailureResponse | dict[str, Any]:
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
