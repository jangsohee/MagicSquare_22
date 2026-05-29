"""Two-cell magic square solver (FR-05 / D-SOL)."""

from __future__ import annotations

from magicsquare.entity.errors import UnsolvableDomainError
from magicsquare.entity.services.empty_cell_locator import find_blank_coords
from magicsquare.entity.services.magic_square_validator import is_magic_square
from magicsquare.entity.services.missing_number_finder import find_not_exist_nums


def _copy_grid(grid: list[list[int]]) -> list[list[int]]:
    """Return a deep copy of ``grid``."""
    return [row[:] for row in grid]


def _filled_grid(
    grid: list[list[int]],
    r1: int,
    c1: int,
    n1: int,
    r2: int,
    c2: int,
    n2: int,
) -> list[list[int]]:
    """Return ``grid`` with ``n1`` and ``n2`` placed at 1-indexed coordinates."""
    filled = _copy_grid(grid)
    filled[r1 - 1][c1 - 1] = n1
    filled[r2 - 1][c2 - 1] = n2
    return filled


def solution(grid: list[list[int]]) -> list[int]:
    """Solve a partial 4×4 grid with exactly two empty cells.

    Args:
        grid: Partial grid with two ``0`` cells and missing values ``{a,b}``.

    Returns:
        Six-element solution ``[r1, c1, n1, r2, c2, n2]`` using 1-indexed
        coordinates. Smaller missing value is tried at the first blank first;
        if that fails, reverse assignment is attempted.

    Raises:
        UnsolvableDomainError: When neither assignment yields a magic square.
    """
    coords = find_blank_coords(grid)
    missing = find_not_exist_nums(grid)
    if len(coords) != 2 or len(missing) != 2:
        raise UnsolvableDomainError()

    (r1, c1), (r2, c2) = coords
    n_small, n_large = missing[0], missing[1]

    forward = _filled_grid(grid, r1, c1, n_small, r2, c2, n_large)
    if is_magic_square(forward):
        return [r1, c1, n_small, r2, c2, n_large]

    reverse = _filled_grid(grid, r1, c1, n_large, r2, c2, n_small)
    if is_magic_square(reverse):
        return [r1, c1, n_large, r2, c2, n_small]

    raise UnsolvableDomainError()
