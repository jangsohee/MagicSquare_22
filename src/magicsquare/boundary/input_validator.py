"""Boundary input validation."""

from __future__ import annotations

from magicsquare.boundary.schemas import (
    INVALID_SIZE_CODE,
    INVALID_SIZE_MESSAGE,
    FailureResponse,
)


class InputValidator:
    """Validates grid input before Domain entry."""

    def validate(
        self, grid: list[list[int]] | None
    ) -> FailureResponse | None:
        """Validate grid input for Boundary entry.

        Args:
            grid: 4x4 grid with exactly two empty cells, or ``None``.

        Returns:
            Failure envelope when validation fails; ``None`` when input passes
            checks implemented so far.
        """
        if grid is None:
            return FailureResponse(
                status="ERROR",
                code=INVALID_SIZE_CODE,
                message=INVALID_SIZE_MESSAGE,
            )
        return None
