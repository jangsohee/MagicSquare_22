"""End-to-end solve use case with optional persistence."""

from __future__ import annotations

from magicsquare.boundary.input_validator import InputValidator
from magicsquare.boundary.schemas import FailureResponse, SuccessResponse
from magicsquare.control.solve_partial_magic_square import SolvePartialMagicSquare
from magicsquare.data.in_memory_matrix_repository import InMemoryMatrixRepository


class SolveMagicSquareUseCase:
    """Orchestrate validate → solve → optional save for integration path."""

    def __init__(
        self,
        repository: InMemoryMatrixRepository,
        solver: SolvePartialMagicSquare | None = None,
    ) -> None:
        """Initialize with repository and optional solver injection."""
        self._repository = repository
        self._solver = solver or SolvePartialMagicSquare()

    def execute(
        self,
        grid: list[list[int]] | None,
        session_id: str,
    ) -> FailureResponse | SuccessResponse:
        """Validate, solve, and persist grid/result on success.

        Args:
            grid: Raw 4x4 grid input, possibly ``None``.
            session_id: Session key for persistence.

        Returns:
            ERROR envelope on validation or domain failure, otherwise OK.
        """
        failure = InputValidator().validate(grid)
        if failure is not None:
            return failure
        assert grid is not None
        response = self._solver.execute(grid)
        if response["status"] == "OK":
            self._repository.save_grid(session_id, grid)
            self._repository.save_result(session_id, response["result"])
        return response
