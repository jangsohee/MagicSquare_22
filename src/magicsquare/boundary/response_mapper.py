"""Map Control/Domain outcomes to Boundary response envelopes."""

from __future__ import annotations

from collections.abc import Callable

from magicsquare.boundary.schemas import (
    ERR_NO_SOLUTION_CODE,
    ERR_NO_SOLUTION_MESSAGE,
    FailureResponse,
    SuccessResponse,
)
from magicsquare.entity.errors import UnsolvableDomainError


def success_response(result: list[int]) -> SuccessResponse:
    """Build OK envelope from a Domain solution tuple."""
    return SuccessResponse(status="OK", result=result)


def no_solution_failure() -> FailureResponse:
    """Build ERROR envelope for Domain NO_COMPLETION."""
    return FailureResponse(
        status="ERROR",
        code=ERR_NO_SOLUTION_CODE,
        message=ERR_NO_SOLUTION_MESSAGE,
    )


def map_domain_solve(
    execute: Callable[[], list[int]],
) -> SuccessResponse | FailureResponse:
    """Wrap Control execute: solution list or unsolvable → envelope.

    Args:
        execute: Callable that runs Domain solve and returns ``int[6]``.

    Returns:
        OK or ERR_NO_SOLUTION envelope.
    """
    try:
        result = execute()
    except UnsolvableDomainError:
        return no_solution_failure()
    return success_response(result)
