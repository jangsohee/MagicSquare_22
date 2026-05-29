"""UI boundary for magic square solve requests."""

from __future__ import annotations

from magicsquare.boundary.input_validator import InputValidator
from magicsquare.boundary.schemas import FailureResponse, SuccessResponse
from magicsquare.control.solve_partial_magic_square import SolvePartialMagicSquare


class UIBoundary:
    """Boundary facade: validate input then delegate to Control."""

    def __init__(
        self,
        use_case: SolvePartialMagicSquare | None = None,
    ) -> None:
        """Initialize with optional use-case injection for testing."""
        self._use_case = use_case or SolvePartialMagicSquare()

    def solve(
        self, grid: list[list[int]] | None
    ) -> FailureResponse | SuccessResponse:
        """Validate grid and solve when input passes Boundary checks.

        Args:
            grid: Raw 4x4 grid input, possibly ``None``.

        Returns:
            ERROR envelope on validation failure, otherwise Control output.
        """
        failure = InputValidator().validate(grid)
        if failure is not None:
            return failure
        assert grid is not None
        return self._use_case.execute(grid)
