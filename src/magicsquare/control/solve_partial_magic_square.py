"""Solve partial magic square use case (Control layer)."""

from __future__ import annotations

from magicsquare.boundary.schemas import (
    ERR_NO_SOLUTION_CODE,
    ERR_NO_SOLUTION_MESSAGE,
    FailureResponse,
    SuccessResponse,
)
from magicsquare.entity.errors import UnsolvableDomainError
from magicsquare.entity.services.two_cell_solver import solution


class SolvePartialMagicSquare:
    """Orchestrates Domain solve for a validated partial grid."""

    def execute(
        self, grid: list[list[int]]
    ) -> SuccessResponse | FailureResponse:
        """Run Domain solver on a validated grid.

        Args:
            grid: Validated 4x4 partial grid with exactly two empty cells.

        Returns:
            OK envelope on success, ERROR envelope on NO_COMPLETION.
        """
        try:
            result = solution(grid)
        except UnsolvableDomainError:
            return FailureResponse(
                status="ERROR",
                code=ERR_NO_SOLUTION_CODE,
                message=ERR_NO_SOLUTION_MESSAGE,
            )
        return SuccessResponse(status="OK", result=result)
