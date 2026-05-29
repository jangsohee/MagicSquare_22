"""Track B RED skeleton — D-SOL-01~04 two-cell solver.

FR-05 | solution() on G1/G2/G3 partial grids.
Domain Mock 금지.
"""

from __future__ import annotations

import pytest

from magicsquare.entity.services.two_cell_solver import solution


class TestDSolTwoCellSolver:
    """D-SOL-01~04 | FR-05 — solution() output contract (I8~I10)."""

    def test_d_sol_01_g1_returns_expected_solution_tuple(self) -> None:
        """D-SOL-01 | G1 → [2,2,7,3,3,10]."""
        # Given
        # grid = G1

        # When
        # result = solution(grid)

        # Then — [2, 2, 7, 3, 3, 10]
        pytest.fail("RED: D-SOL-01 — G1 → solution [2,2,7,3,3,10]")

    def test_d_sol_02_g2_returns_reverse_assignment_tuple(self) -> None:
        """D-SOL-02 | G2 DT-06 → [1,1,16,4,4,1] (G2 TBD)."""
        # Given
        # grid = G2  # DT-06 placeholder

        # When
        # result = solution(grid)

        # Then — [1, 1, 16, 4, 4, 1]
        pytest.fail("RED: D-SOL-02 — G2 TBD")

    def test_d_sol_03_g3_raises_unsolvable_domain_error(self) -> None:
        """D-SOL-03 | G3 DT-10 → UnsolvableDomainError."""
        # Given
        # grid = G3

        # When
        # result = solution(grid)

        # Then — UnsolvableDomainError / NO_COMPLETION
        pytest.fail("RED: D-SOL-03 — G3 → UnsolvableDomainError")

    def test_d_sol_04_g1_output_len_six_one_index_coords(self) -> None:
        """D-SOL-04 | G1 → len=6, coords 1-index."""
        # Given
        # grid = G1

        # When
        # result = solution(grid)

        # Then — len(result)==6; r,c coords in [1,4]
        pytest.fail("RED: D-SOL-04 — G1 → len=6, coords 1-index")
