"""Entity layer — domain data and invariants."""

from magicsquare.entity.errors import UserValidationError
from magicsquare.entity.user import User

__all__ = ["User", "UserValidationError"]
