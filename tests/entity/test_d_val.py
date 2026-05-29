"""Track B RED skeleton — D-VAL-01~06 magic square validation.

FR-04 | is_magic_square on G0 and derived invalid grids.
Domain Mock 금지.
"""

from __future__ import annotations

import pytest

from magicsquare.entity.services.magic_square_validator import is_magic_square


class TestDValMagicSquareValidator:
    """D-VAL-01~06 | FR-04 — is_magic_square invariant checks (I1~I5)."""

    def test_d_val_01_g0_complete_magic_returns_true(self) -> None:
        """D-VAL-01 | G0 FIX-MAGIC → true."""
        # Given
        # grid = G0

        # When
        # result = is_magic_square(grid)

        # Then — true
        pytest.fail("RED: D-VAL-01 — G0 complete magic → true")

    def test_d_val_02_g0_broken_row_sum_returns_false(self) -> None:
        """D-VAL-02 | G0 with broken row sum → false."""
        # Given
        # grid = G0 with row 0 sum != 34

        # When
        # result = is_magic_square(grid)

        # Then — false
        pytest.fail("RED: D-VAL-02 — G0 broken row sum → false")

    def test_d_val_03_g0_broken_col_sum_returns_false(self) -> None:
        """D-VAL-03 | G0 with broken column sum → false."""
        # Given
        # grid = G0 with column sum != 34

        # When
        # result = is_magic_square(grid)

        # Then — false
        pytest.fail("RED: D-VAL-03 — G0 broken column sum → false")

    def test_d_val_04_g0_broken_diagonal_returns_false(self) -> None:
        """D-VAL-04 | G0 with broken diagonal → false."""
        # Given
        # grid = G0 with main/anti diagonal sum != 34

        # When
        # result = is_magic_square(grid)

        # Then — false
        pytest.fail("RED: D-VAL-04 — G0 broken diagonal → false")

    def test_d_val_05_grid_violates_one_to_sixteen_returns_false(self) -> None:
        """D-VAL-05 | values outside 1~16 → false."""
        # Given
        # grid = 4×4 with value 17 or duplicate breaking 1~16 set

        # When
        # result = is_magic_square(grid)

        # Then — false
        pytest.fail("RED: D-VAL-05 — 1~16 set violation → false")

    def test_d_val_06_complete_grid_with_zero_returns_false(self) -> None:
        """D-VAL-06 | complete grid containing 0 → false."""
        # Given
        # grid = G0-like 4×4 with a 0 cell among otherwise filled cells

        # When
        # result = is_magic_square(grid)

        # Then — false
        pytest.fail("RED: D-VAL-06 — complete grid with 0 → false")
