"""Entity value objects for magic square domain rules."""

from __future__ import annotations


class MagicConstant:
    """Single source for magic square line-sum target (NFR-08)."""

    GRID_SIZE: int = 4
    TARGET_LINE_SUM: int = 34
    REQUIRED_EMPTY_CELLS: int = 2
    MAX_CELL_VALUE: int = GRID_SIZE * GRID_SIZE
