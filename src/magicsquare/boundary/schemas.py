"""Boundary response schemas."""

from __future__ import annotations

from typing import Literal, TypedDict

INVALID_SIZE_CODE = "INVALID_SIZE"
INVALID_SIZE_MESSAGE = "Grid must be 4x4."

ERR_GRID_ROWS_CODE = "ERR_GRID_ROWS"
ERR_GRID_ROWS_MESSAGE = "Grid must have exactly 4 rows."

ERR_GRID_COLS_CODE = "ERR_GRID_COLS"
ERR_GRID_COLS_MESSAGE = "Each row must have exactly 4 columns."

ERR_VALUE_RANGE_CODE = "ERR_VALUE_RANGE"
ERR_VALUE_RANGE_MESSAGE = (
    "Cell value must be 0 or between 1 and 16 inclusive."
)


class FailureResponse(TypedDict):
    """ERROR envelope returned when Boundary validation fails."""

    status: Literal["ERROR"]
    code: str
    message: str
