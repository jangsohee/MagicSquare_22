"""Track B RED skeleton — D-MIS-01 missing numbers.

FR-03 | find_not_exist_nums(G1) → {7, 10} ascending.
Domain Mock 금지.
"""

from __future__ import annotations

import pytest

from magicsquare.entity.services.missing_number_finder import find_not_exist_nums


class TestDMis01MissingNumbers:
    """D-MIS-01 | FR-03 — missing number pair from partial grid."""

    def test_d_mis_01_g1_returns_seven_and_ten_ascending(self) -> None:
        """D-MIS-01 | G1 → {7, 10} ascending."""
        # Given
        # grid = G1

        # When
        # missing = find_not_exist_nums(grid)

        # Then — [7, 10] ascending
        pytest.fail("RED: D-MIS-01 — G1 → missing numbers {7, 10} ascending")
