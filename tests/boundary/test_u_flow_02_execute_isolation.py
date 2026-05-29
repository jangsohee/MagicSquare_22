"""Boundary tests for U-FLOW-02 execute isolation (FR-01).

Invalid input → SolvePartialMagicSquare.execute call_count==0.
A-07 scope: E004/E005 only (null isolation covered by A-01 / UT-01).
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from magicsquare.boundary.ui_boundary import UIBoundary

# E004 — value range violation (UT-04)
E004_GRID: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 17],
]

# E005 — duplicate non-zero (UT-08)
E005_GRID: list[list[int]] = [
    [16, 3, 2, 0],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 5, 0],
]


class TestUFlow02ExecuteIsolation:
    """U-FLOW-02 | FR-01 — Domain execute never invoked on invalid input."""

    @patch(
        "magicsquare.control.solve_partial_magic_square.SolvePartialMagicSquare.execute"
    )
    def test_u_flow_02_extended_e004_execute_zero_calls(
        self, mock_execute: MagicMock
    ) -> None:
        """U-FLOW-02 ext | E004 invalid grid → execute call_count==0."""
        # U-FLOW-02
        # Given
        boundary = UIBoundary()
        grid = [row[:] for row in E004_GRID]

        # When
        response = boundary.solve(grid)

        # Then
        assert response["status"] == "ERROR"
        mock_execute.assert_not_called()

    @patch(
        "magicsquare.control.solve_partial_magic_square.SolvePartialMagicSquare.execute"
    )
    def test_u_flow_02_extended_e005_execute_zero_calls(
        self, mock_execute: MagicMock
    ) -> None:
        """U-FLOW-02 ext | E005 invalid grid → execute call_count==0."""
        # U-FLOW-02
        # Given
        boundary = UIBoundary()
        grid = [row[:] for row in E005_GRID]

        # When
        response = boundary.solve(grid)

        # Then
        assert response["status"] == "ERROR"
        mock_execute.assert_not_called()
