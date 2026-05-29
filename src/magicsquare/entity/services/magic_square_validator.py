"""Magic square validation service (FR-04 / D-VAL)."""

from __future__ import annotations

from magicsquare.entity.magic_constant import MagicConstant


def is_magic_square(grid: list[list[int]]) -> bool:
    """Return whether ``grid`` is a complete 4×4 magic square.

    Args:
        grid: 4×4 grid of cell values.

    Returns:
        ``True`` when all values are 1..16 exactly once and every row,
        column, and diagonal sums to ``MagicConstant.TARGET_LINE_SUM``.
    """
    if len(grid) != 4:
        return False
    for row in grid:
        if len(row) != 4:
            return False

    values: list[int] = [cell for row in grid for cell in row]
    if any(cell == 0 for cell in values):
        return False
    if any(cell < 1 or cell > 16 for cell in values):
        return False
    if len(set(values)) != 16:
        return False

    target = MagicConstant.TARGET_LINE_SUM
    for row in grid:
        if sum(row) != target:
            return False
    for col in range(4):
        if sum(grid[row][col] for row in range(4)) != target:
            return False
    if sum(grid[i][i] for i in range(4)) != target:
        return False
    if sum(grid[i][3 - i] for i in range(4)) != target:
        return False
    return True
