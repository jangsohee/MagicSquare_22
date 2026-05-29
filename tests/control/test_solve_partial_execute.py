"""Control tests for ``SolvePartialMagicSquare.execute`` (Report/16 P0)."""

from __future__ import annotations

import pytest

from magicsquare.boundary.example_grids import UT09_PARTIAL_GRID, UT09_PARTIAL_RESULT
from magicsquare.boundary.response_mapper import map_domain_solve
from magicsquare.boundary.schemas import (
    ERR_NO_SOLUTION_CODE,
    ERR_NO_SOLUTION_MESSAGE,
)
from magicsquare.control.solve_partial_magic_square import SolvePartialMagicSquare
from magicsquare.entity.errors import UnsolvableDomainError

# DT-10 / IT-FAIL-02 unsolvable partial grid
G3_UNSOLVABLE_GRID: list[list[int]] = [
    [16, 0, 2, 13],
    [5, 10, 0, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 3],
]


class TestSolvePartialExecute:
    """Control execute — Domain tuple or unsolvable (no Boundary envelope)."""

    def test_execute_valid_grid_returns_int_six_tuple(self) -> None:
        """Valid UT-09 grid → ``list[int]`` length 6."""
        # Control-EXEC-01
        solver = SolvePartialMagicSquare()
        grid = [row[:] for row in UT09_PARTIAL_GRID]

        result = solver.execute(grid)

        assert result == UT09_PARTIAL_RESULT
        assert len(result) == 6

    def test_execute_unsolvable_grid_raises_unsolvable_domain_error(self) -> None:
        """G3 unsolvable → ``UnsolvableDomainError`` (mapper maps to E007)."""
        # Control-EXEC-02
        solver = SolvePartialMagicSquare()
        grid = [row[:] for row in G3_UNSOLVABLE_GRID]

        with pytest.raises(UnsolvableDomainError):
            solver.execute(grid)

    def test_mapper_wraps_unsolvable_as_err_no_solution(self) -> None:
        """Boundary mapper → ERR_NO_SOLUTION envelope when execute raises."""
        # Control-EXEC-03
        solver = SolvePartialMagicSquare()
        grid = [row[:] for row in G3_UNSOLVABLE_GRID]

        response = map_domain_solve(lambda: solver.execute(grid))

        assert response["status"] == "ERROR"
        assert response["code"] == ERR_NO_SOLUTION_CODE
        assert response["message"] == ERR_NO_SOLUTION_MESSAGE
