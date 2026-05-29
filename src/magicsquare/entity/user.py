"""User domain entity — identity and display name invariants."""

from __future__ import annotations

from dataclasses import dataclass

from magicsquare.entity.errors import UserValidationError

USER_ID_MAX_LENGTH = 64
DISPLAY_NAME_MAX_LENGTH = 100


def _validate_user_id(user_id: str) -> str:
    """Validate and normalize a user identifier.

    Args:
        user_id: Raw user identifier.

    Returns:
        Stripped non-empty user identifier within length limit.

    Raises:
        UserValidationError: If ``user_id`` is empty or exceeds max length.
    """
    normalized = user_id.strip()
    if not normalized:
        raise UserValidationError(
            "INVALID_USER_ID",
            "user_id must not be empty or whitespace-only.",
        )
    if len(normalized) > USER_ID_MAX_LENGTH:
        raise UserValidationError(
            "INVALID_USER_ID",
            f"user_id must be at most {USER_ID_MAX_LENGTH} characters.",
        )
    return normalized


def _validate_display_name(display_name: str) -> str:
    """Validate and normalize a display name.

    Args:
        display_name: Raw display name.

    Returns:
        Stripped non-empty display name within length limit.

    Raises:
        UserValidationError: If ``display_name`` is empty or exceeds max length.
    """
    normalized = display_name.strip()
    if not normalized:
        raise UserValidationError(
            "INVALID_DISPLAY_NAME",
            "display_name must not be empty or whitespace-only.",
        )
    if len(normalized) > DISPLAY_NAME_MAX_LENGTH:
        raise UserValidationError(
            "INVALID_DISPLAY_NAME",
            f"display_name must be at most {DISPLAY_NAME_MAX_LENGTH} characters.",
        )
    return normalized


@dataclass(frozen=True, slots=True, eq=True)
class User:
    """Domain entity representing a MagicSquare session user.

    Invariants:
        - ``user_id`` is non-empty after strip, max ``USER_ID_MAX_LENGTH``.
        - ``display_name`` is non-empty after strip, max ``DISPLAY_NAME_MAX_LENGTH``.
        - Instances are immutable (frozen dataclass).

    Attributes:
        user_id: Stable user identifier for data layer session keys.
        display_name: Human-readable label shown at boundary layer.
    """

    user_id: str
    display_name: str

    def __post_init__(self) -> None:
        """Apply entity invariants after dataclass initialization."""
        object.__setattr__(self, "user_id", _validate_user_id(self.user_id))
        object.__setattr__(
            self,
            "display_name",
            _validate_display_name(self.display_name),
        )

    @classmethod
    def create(cls, user_id: str, display_name: str) -> User:
        """Create a validated User entity.

        Args:
            user_id: Stable user identifier.
            display_name: Human-readable display name.

        Returns:
            Immutable ``User`` instance satisfying entity invariants.

        Raises:
            UserValidationError: If any invariant is violated.
        """
        return cls(user_id=user_id, display_name=display_name)
