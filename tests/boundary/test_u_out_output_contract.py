"""Track A RED skeleton — U-OUT-* success output contract.

Given valid G1 partial grid; UIBoundary.solve returns int[6] 1-index Success envelope.
U-OUT-01/02/03: len, coords, missing-number values in result tuple.
"""

from __future__ import annotations

import pytest

from magicsquare.boundary.ui_boundary import UIBoundary


class TestUOutOutputContract:
    """U-OUT-01~03 | FR-02/FR-05 — Boundary success output shape."""

    def test_u_out_01_g1_solve_returns_six_element_result(self) -> None:
        """U-OUT-01 | G1 → len(result)==6, status OK."""
        # Given
        # matrix = G1  # blanks (2,2),(3,3); missing {7,10}
        # boundary = UIBoundary()
        # mock execute → [2, 2, 7, 3, 3, 10]

        # When
        # response = boundary.solve(matrix)

        # Then — status OK; len(result)==6
        pytest.fail("RED: U-OUT-01 — G1 solve → len(result)==6, status OK")

    def test_u_out_02_g1_solve_coords_are_one_indexed(self) -> None:
        """U-OUT-02 | G1 → r,c ∈ [1,4] 1-index."""
        # Given
        # matrix = G1
        # boundary = UIBoundary()
        # mock execute → [2, 2, 7, 3, 3, 10]

        # When
        # response = boundary.solve(matrix)

        # Then — result[0], result[1], result[3], result[4] each in [1,4]
        pytest.fail("RED: U-OUT-02 — G1 solve → coords 1-index in [1,4]")

    def test_u_out_03_g1_solve_result_matches_expected_tuple(self) -> None:
        """U-OUT-03 | G1 → result == [2,2,7,3,3,10] (boundary passthrough)."""
        # Given
        # matrix = G1
        # boundary = UIBoundary()
        # mock SolvePartialMagicSquare.execute → [2, 2, 7, 3, 3, 10]

        # When
        # response = boundary.solve(matrix)

        # Then — result equals [2,2,7,3,3,10] without reorder
        pytest.fail("RED: U-OUT-03 — G1 solve → result [2,2,7,3,3,10] passthrough")
