"""Boundary input validation."""

from __future__ import annotations

from magicsquare.boundary.schemas import (
    ERR_DUPLICATE_CODE,
    ERR_EMPTY_COUNT_CODE,
    ERR_EMPTY_COUNT_MESSAGE,
    ERR_GRID_COLS_CODE,
    ERR_GRID_COLS_MESSAGE,
    ERR_GRID_ROWS_CODE,
    ERR_GRID_ROWS_MESSAGE,
    ERR_VALUE_RANGE_CODE,
    ERR_VALUE_RANGE_MESSAGE,
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
        if len(grid) != 4:
            return FailureResponse(
                status="ERROR",
                code=ERR_GRID_ROWS_CODE,
                message=ERR_GRID_ROWS_MESSAGE,
            )
        for row in grid:
            if len(row) != 4:
                return FailureResponse(
                    status="ERROR",
                    code=ERR_GRID_COLS_CODE,
                    message=ERR_GRID_COLS_MESSAGE,
                )
        for row in grid:
            for cell in row:
                if cell != 0 and not 1 <= cell <= 16:
                    return FailureResponse(
                        status="ERROR",
                        code=ERR_VALUE_RANGE_CODE,
                        message=ERR_VALUE_RANGE_MESSAGE,
                    )
        empty_count = sum(cell == 0 for row in grid for cell in row)
        if empty_count != 2:
            return FailureResponse(
                status="ERROR",
                code=ERR_EMPTY_COUNT_CODE,
                message=ERR_EMPTY_COUNT_MESSAGE,
            )
        seen: set[int] = set()
        for row in grid:
            for cell in row:
                if cell == 0:
                    continue
                if cell in seen:
                    return FailureResponse(
                        status="ERROR",
                        code=ERR_DUPLICATE_CODE,
                        message=f"Duplicate non-zero value: {cell}.",
                    )
                seen.add(cell)
        return None
