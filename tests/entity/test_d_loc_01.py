"""Track B tests — D-LOC-01 blank cell coordinates.

FR-02 | find_blank_coords(G1) → (2,2), (3,3) row-major, 1-index.
Domain Mock 금지.
"""

from __future__ import annotations

from magicsquare.entity.services.empty_cell_locator import find_blank_coords

G1_PARTIAL: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]


class TestDLoc01BlankCoords:
    """D-LOC-01 | FR-02 — row-major blank coordinate discovery."""

    def test_d_loc_01_g1_returns_row_major_blank_coords(self) -> None:
        """D-LOC-01 | G1 → (2,2), (3,3) 1-index."""
        # D-LOC-01
        # Given
        grid = [row[:] for row in G1_PARTIAL]

        # When
        coords = find_blank_coords(grid)

        # Then
        assert coords == [(2, 2), (3, 3)]
