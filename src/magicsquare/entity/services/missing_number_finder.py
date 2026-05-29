"""Missing number discovery for partial grids (FR-03 / D-MIS)."""

from __future__ import annotations

from magicsquare.entity.magic_constant import MagicConstant


def find_not_exist_nums(grid: list[list[int]]) -> list[int]:
    """Return missing values from ``1..16`` not present in the grid.

    Args:
        grid: Partial 4×4 grid; ``0`` cells are ignored.

    Returns:
        Ascending list of integers absent from non-zero cells.
    """
    present = {cell for row in grid for cell in row if cell != 0}
    upper = MagicConstant.GRID_SIZE * MagicConstant.GRID_SIZE
    return [value for value in range(1, upper + 1) if value not in present]
