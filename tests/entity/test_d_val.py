"""Track B tests — D-VAL-01~06 magic square validation.

FR-04 | is_magic_square on G0 and derived invalid grids.
Domain Mock 금지.
"""

from __future__ import annotations

from magicsquare.entity.services.magic_square_validator import is_magic_square

G0_FIX_MAGIC: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]


def _copy_grid(grid: list[list[int]]) -> list[list[int]]:
    """Return a deep copy of a 4×4 grid."""
    return [row[:] for row in grid]


class TestDValMagicSquareValidator:
    """D-VAL-01~06 | FR-04 — is_magic_square invariant checks (I1~I5)."""

    def test_d_val_01_g0_complete_magic_returns_true(self) -> None:
        """D-VAL-01 | G0 FIX-MAGIC → true."""
        # D-VAL-01
        # Given
        grid = _copy_grid(G0_FIX_MAGIC)

        # When
        result = is_magic_square(grid)

        # Then
        assert result is True

    def test_d_val_02_g0_broken_row_sum_returns_false(self) -> None:
        """D-VAL-02 | G0 with broken row sum → false."""
        # D-VAL-02
        # Given
        grid = _copy_grid(G0_FIX_MAGIC)
        grid[0][0] = 15

        # When
        result = is_magic_square(grid)

        # Then
        assert result is False

    def test_d_val_03_g0_broken_col_sum_returns_false(self) -> None:
        """D-VAL-03 | G0 with broken column sum → false."""
        # D-VAL-03
        # Given
        grid = _copy_grid(G0_FIX_MAGIC)
        grid[0][1] = 4

        # When
        result = is_magic_square(grid)

        # Then
        assert result is False

    def test_d_val_04_g0_broken_diagonal_returns_false(self) -> None:
        """D-VAL-04 | G0 with broken diagonal → false."""
        # D-VAL-04
        # Given
        grid = _copy_grid(G0_FIX_MAGIC)
        grid[0][0] = 15

        # When
        result = is_magic_square(grid)

        # Then
        assert result is False

    def test_d_val_05_grid_violates_one_to_sixteen_returns_false(self) -> None:
        """D-VAL-05 | values outside 1~16 → false."""
        # D-VAL-05
        # Given
        grid = _copy_grid(G0_FIX_MAGIC)
        grid[3][3] = 17

        # When
        result = is_magic_square(grid)

        # Then
        assert result is False

    def test_d_val_06_complete_grid_with_zero_returns_false(self) -> None:
        """D-VAL-06 | complete grid containing 0 → false."""
        # D-VAL-06
        # Given
        grid = _copy_grid(G0_FIX_MAGIC)
        grid[3][3] = 0

        # When
        result = is_magic_square(grid)

        # Then
        assert result is False
