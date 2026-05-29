"""In-memory matrix repository (Report/02 ST-01~02)."""

from __future__ import annotations

from dataclasses import dataclass


class DataError(Exception):
    """Raised when a Data layer operation fails."""

    NOT_FOUND = "NOT_FOUND"


@dataclass
class _Record:
    """Stored grid and optional solve result for a session id."""

    grid: list[list[int]]
    result: list[int] | None = None


class InMemoryMatrixRepository:
    """In-memory persistence for grid and solve result round-trip."""

    def __init__(self) -> None:
        """Initialize an empty in-memory store."""
        self._records: dict[str, _Record] = {}

    def save_grid(self, session_id: str, grid: list[list[int]]) -> None:
        """Persist a 4x4 grid for ``session_id``.

        Args:
            session_id: Non-empty session identifier.
            grid: Grid to store (deep-copied).
        """
        self._records[session_id] = _Record(grid=[row[:] for row in grid])

    def load_grid(self, session_id: str) -> list[list[int]]:
        """Load a stored grid by session id.

        Args:
            session_id: Session identifier.

        Returns:
            Deep copy of the stored 4x4 grid.

        Raises:
            DataError: When no record exists for ``session_id``.
        """
        record = self._records.get(session_id)
        if record is None:
            raise DataError(DataError.NOT_FOUND)
        return [row[:] for row in record.grid]

    def save_result(self, session_id: str, result: list[int]) -> None:
        """Persist a six-element solve result for an existing session.

        Args:
            session_id: Session identifier with a saved grid.
            result: Six-element solve output (copied).

        Raises:
            DataError: When no record exists for ``session_id``.
        """
        record = self._records.get(session_id)
        if record is None:
            raise DataError(DataError.NOT_FOUND)
        record.result = result[:]

    def load_result(self, session_id: str) -> list[int]:
        """Load a stored solve result by session id.

        Args:
            session_id: Session identifier.

        Returns:
            Copy of the stored six-element result.

        Raises:
            DataError: When no record or result exists for ``session_id``.
        """
        record = self._records.get(session_id)
        if record is None or record.result is None:
            raise DataError(DataError.NOT_FOUND)
        return record.result[:]
