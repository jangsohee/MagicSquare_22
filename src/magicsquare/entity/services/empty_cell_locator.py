"""Blank cell coordinate discovery (FR-02 / D-LOC)."""

from __future__ import annotations


def find_blank_coords(grid: list[list[int]]) -> list[tuple[int, int]]:
    """Return 1-indexed coordinates of empty cells in row-major order.

    Args:
        grid: Partial 4×4 grid with ``0`` marking empty cells.

    Returns:
        List of ``(row, col)`` tuples using 1-based indexing.
    """
    coords: list[tuple[int, int]] = []
    for row_index, row in enumerate(grid):
        for col_index, cell in enumerate(row):
            if cell == 0:
                coords.append((row_index + 1, col_index + 1))
    return coords
