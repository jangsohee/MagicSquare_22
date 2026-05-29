"""Solve partial magic square use case (Control layer)."""

from __future__ import annotations

from magicsquare.entity.services.two_cell_solver import (
    solution as solve_two_cell_partial_grid,
)


class SolvePartialMagicSquare:
    """Orchestrates Domain solve for a validated partial grid."""

    def execute(self, grid: list[list[int]]) -> list[int]:
        """Run Domain solver on a validated grid.

        Args:
            grid: Validated 4x4 partial grid with exactly two empty cells.

        Returns:
            Six-element solution tuple (1-index coordinates and values).

        Raises:
            UnsolvableDomainError: When no magic completion exists.
        """
        return solve_two_cell_partial_grid(grid)
