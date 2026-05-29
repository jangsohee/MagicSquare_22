"""Track B RED skeleton — D-LOC-01 blank cell coordinates.

FR-02 | find_blank_coords(G1) → (2,2), (3,3) row-major, 1-index.
Domain Mock 금지.
"""

from __future__ import annotations

import pytest

from magicsquare.entity.services.empty_cell_locator import find_blank_coords


class TestDLoc01BlankCoords:
    """D-LOC-01 | FR-02 — row-major blank coordinate discovery."""

    def test_d_loc_01_g1_returns_row_major_blank_coords(self) -> None:
        """D-LOC-01 | G1 → (2,2), (3,3) 1-index."""
        # Given
        # grid = G1

        # When
        # coords = find_blank_coords(grid)

        # Then — (2,2), (3,3) row-major
        pytest.fail("RED: D-LOC-01 — G1 → blank coords (2,2), (3,3) row-major")
