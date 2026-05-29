"""Domain-level errors for entity layer."""

from __future__ import annotations


class UserValidationError(ValueError):
    """Raised when User entity invariants are violated.

    This error belongs to the entity layer. Boundary layer maps it to
    external error responses; it must not carry UI message contracts.
    """

    def __init__(self, code: str, message: str) -> None:
        """Initialize a user validation error.

        Args:
            code: Stable machine-readable error code (e.g. ``INVALID_USER_ID``).
            message: Human-readable explanation for developers and tests.
        """
        self.code = code
        super().__init__(message)


class UnsolvableDomainError(Exception):
    """Raised when no magic square completion exists for a partial grid."""

    def __init__(self, code: str = "NO_COMPLETION", message: str = "") -> None:
        """Initialize an unsolvable grid error.

        Args:
            code: Stable machine-readable error code.
            message: Human-readable explanation for developers and tests.
        """
        self.code = code
        super().__init__(message or "No magic square completion exists.")
