"""Track B tests — D-MIS-01 missing numbers.

FR-03 | find_not_exist_nums(G1) → {7, 10} ascending.
Domain Mock 금지.
"""

from __future__ import annotations

from magicsquare.entity.services.missing_number_finder import find_not_exist_nums

G1_PARTIAL: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]


class TestDMis01MissingNumbers:
    """D-MIS-01 | FR-03 — missing number pair from partial grid."""

    def test_d_mis_01_g1_returns_seven_and_ten_ascending(self) -> None:
        """D-MIS-01 | G1 → {7, 10} ascending."""
        # D-MIS-01
        # Given
        grid = [row[:] for row in G1_PARTIAL]

        # When
        missing = find_not_exist_nums(grid)

        # Then
        assert missing == [7, 10]
