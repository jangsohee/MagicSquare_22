"""Track A RED skeleton — U-FLOW-02 execute isolation (extended).

Invalid input → SolvePartialMagicSquare.execute call_count==0.
Extensions cover representative E004/E005 invalid grids (null covered by U-IN-01).
"""

from __future__ import annotations

import pytest

from magicsquare.boundary.ui_boundary import UIBoundary


class TestUFlow02ExecuteIsolation:
    """U-FLOW-02 | FR-01 — Domain execute never invoked on invalid input."""

    def test_u_flow_02_invalid_null_execute_zero_calls(self) -> None:
        """U-FLOW-02 | null grid → execute spy call_count==0."""
        # Given
        # matrix = None
        # boundary = UIBoundary()
        # spy: patch SolvePartialMagicSquare.execute

        # When
        # boundary.solve(matrix)

        # Then — execute.call_count == 0
        pytest.fail("RED: U-FLOW-02 — invalid null → execute call_count==0")

    def test_u_flow_02_extended_e004_execute_zero_calls(self) -> None:
        """U-FLOW-02 ext | E004 invalid grid → execute call_count==0."""
        # Given
        # matrix = grid with cell=17
        # boundary = UIBoundary()
        # spy: patch SolvePartialMagicSquare.execute

        # When
        # boundary.solve(matrix)

        # Then — execute.call_count == 0
        pytest.fail("RED: U-FLOW-02 ext — E004 invalid → execute call_count==0")

    def test_u_flow_02_extended_e005_execute_zero_calls(self) -> None:
        """U-FLOW-02 ext | E005 invalid grid → execute call_count==0."""
        # Given
        # matrix = grid with duplicate non-zero 5
        # boundary = UIBoundary()
        # spy: patch SolvePartialMagicSquare.execute

        # When
        # boundary.solve(matrix)

        # Then — execute.call_count == 0
        pytest.fail("RED: U-FLOW-02 ext — E005 invalid → execute call_count==0")
