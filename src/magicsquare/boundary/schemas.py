"""Boundary response schemas."""

from __future__ import annotations

from typing import Literal, TypedDict

INVALID_SIZE_CODE = "INVALID_SIZE"
INVALID_SIZE_MESSAGE = "Grid must be 4x4."

ERR_GRID_ROWS_CODE = "ERR_GRID_ROWS"
ERR_GRID_ROWS_MESSAGE = "Grid must have exactly 4 rows."


class FailureResponse(TypedDict):
    """ERROR envelope returned when Boundary validation fails."""

    status: Literal["ERROR"]
    code: str
    message: str
