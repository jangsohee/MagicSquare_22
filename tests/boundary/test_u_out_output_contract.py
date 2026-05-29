"""Boundary tests for U-OUT success output contract (FR-02/FR-05).

Given valid G1 partial grid; validate_and_solve returns int[6] 1-index Success envelope.
U-OUT-01/02/03: len, coords, Domain result passthrough (UX-05).
"""

from __future__ import annotations

from magicsquare.boundary.entry import validate_and_solve

G1_PARTIAL: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]

# B-03 reverse assignment for G1 (Report/09 G1 placeholder).
EXPECTED_G1_RESULT = [2, 2, 10, 3, 3, 7]


class TestUOutOutputContract:
    """U-OUT-01~03 | FR-02/FR-05 — Boundary success output shape."""

    def test_u_out_01_g1_solve_returns_six_element_result(self) -> None:
        """U-OUT-01 | G1 → len(result)==6, status OK."""
        # U-OUT-01
        # Given
        grid = [row[:] for row in G1_PARTIAL]

        # When
        response = validate_and_solve(grid)

        # Then
        assert response["status"] == "OK"
        assert len(response["result"]) == 6

    def test_u_out_02_g1_solve_coords_are_one_indexed(self) -> None:
        """U-OUT-02 | G1 → r,c ∈ [1,4] 1-index."""
        # U-OUT-02
        # Given
        grid = [row[:] for row in G1_PARTIAL]

        # When
        response = validate_and_solve(grid)

        # Then
        result = response["result"]
        assert all(1 <= result[i] <= 4 for i in (0, 1, 3, 4))

    def test_u_out_03_g1_solve_result_matches_expected_tuple(self) -> None:
        """U-OUT-03 | G1 → result passthrough without reorder."""
        # U-OUT-03
        # Given
        grid = [row[:] for row in G1_PARTIAL]

        # When
        response = validate_and_solve(grid)

        # Then
        assert response["result"] == EXPECTED_G1_RESULT
