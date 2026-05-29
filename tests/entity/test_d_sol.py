"""Track B tests — D-SOL-01~04 two-cell solver.

FR-05 | solution() on G1/G2/G3 partial grids.
Domain Mock 금지.
"""

from __future__ import annotations

import pytest

from magicsquare.entity.errors import UnsolvableDomainError
from magicsquare.entity.services.two_cell_solver import solution

G1_PARTIAL: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]

G2_PARTIAL: list[list[int]] = [
    [0, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 0],
]

# DT-10 — neither forward nor reverse assignment completes a magic square.
G3_UNSOLVABLE: list[list[int]] = [
    [16, 0, 2, 13],
    [5, 10, 0, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 3],
]


class TestDSolTwoCellSolver:
    """D-SOL-01~04 | FR-05 — solution() output contract (I8~I10)."""

    def test_d_sol_01_g1_returns_expected_solution_tuple(self) -> None:
        """D-SOL-01 | G1 → [2,2,10,3,3,7] (reverse assignment)."""
        # D-SOL-01
        # Given
        grid = [row[:] for row in G1_PARTIAL]

        # When
        result = solution(grid)

        # Then
        assert result == [2, 2, 10, 3, 3, 7]

    def test_d_sol_02_g2_returns_reverse_assignment_tuple(self) -> None:
        """D-SOL-02 | G2 DT-06 → [1,1,16,4,4,1]."""
        # D-SOL-02
        # Given
        grid = [row[:] for row in G2_PARTIAL]

        # When
        result = solution(grid)

        # Then
        assert result == [1, 1, 16, 4, 4, 1]

    def test_d_sol_03_g3_raises_unsolvable_domain_error(self) -> None:
        """D-SOL-03 | G3 DT-10 → UnsolvableDomainError."""
        # D-SOL-03
        # Given
        grid = [row[:] for row in G3_UNSOLVABLE]

        # When / Then
        with pytest.raises(UnsolvableDomainError):
            solution(grid)

    def test_d_sol_04_g1_output_len_six_one_index_coords(self) -> None:
        """D-SOL-04 | G1 → len=6, coords 1-index."""
        # D-SOL-04
        # Given
        grid = [row[:] for row in G1_PARTIAL]

        # When
        result = solution(grid)

        # Then
        assert len(result) == 6
        assert all(1 <= result[i] <= 4 for i in (0, 1, 3, 4))
