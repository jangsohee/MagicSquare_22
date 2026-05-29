"""Solve partial magic square use case (Control layer)."""

from __future__ import annotations

from magicsquare.boundary.schemas import SuccessResponse
from magicsquare.entity.services.two_cell_solver import solution


class SolvePartialMagicSquare:
    """Orchestrates Domain solve for a validated partial grid."""

    def execute(self, grid: list[list[int]]) -> SuccessResponse:
        """Run Domain solver on a validated grid.

        Args:
            grid: Validated 4x4 partial grid with exactly two empty cells.

        Returns:
            OK envelope with Domain ``int[6]`` result passthrough.
        """
        result = solution(grid)
        return SuccessResponse(status="OK", result=result)
