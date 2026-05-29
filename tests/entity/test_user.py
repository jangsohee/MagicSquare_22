"""Entity-layer tests for User domain entity."""

from __future__ import annotations

import pytest

from magicsquare.entity.errors import UserValidationError
from magicsquare.entity.user import DISPLAY_NAME_MAX_LENGTH, USER_ID_MAX_LENGTH, User


class TestUserCreate:
    """Tests for User.create and entity invariants."""

    def test_user_create_valid(self) -> None:
        """Given valid id and name, When User.create, Then entity is returned."""
        # Arrange
        user_id = " learner-01 "
        display_name = " Magic Learner "

        # Act
        user = User.create(user_id=user_id, display_name=display_name)

        # Assert
        assert user.user_id == "learner-01"
        assert user.display_name == "Magic Learner"

    def test_user_is_immutable(self) -> None:
        """Given a User, When attribute assignment is attempted, Then TypeError."""
        # Arrange
        user = User.create(user_id="u1", display_name="Learner")

        # Act / Assert
        with pytest.raises(AttributeError):
            user.user_id = "changed"  # type: ignore[misc]

    def test_user_equality_by_value(self) -> None:
        """Given two Users with same fields, When compared, Then they are equal."""
        # Arrange
        user_a = User.create(user_id="u1", display_name="Learner")
        user_b = User.create(user_id="u1", display_name="Learner")

        # Act / Assert
        assert user_a == user_b


class TestUserIdValidation:
    """Tests for user_id invariant."""

    def test_user_id_empty_raises(self) -> None:
        """Given empty user_id, When User.create, Then UserValidationError."""
        # Arrange / Act / Assert
        with pytest.raises(UserValidationError) as exc_info:
            User.create(user_id="", display_name="Learner")

        assert exc_info.value.code == "INVALID_USER_ID"

    def test_user_id_whitespace_only_raises(self) -> None:
        """Given whitespace user_id, When User.create, Then UserValidationError."""
        # Arrange / Act / Assert
        with pytest.raises(UserValidationError) as exc_info:
            User.create(user_id="   ", display_name="Learner")

        assert exc_info.value.code == "INVALID_USER_ID"

    def test_user_id_exceeds_max_length_raises(self) -> None:
        """Given too long user_id, When User.create, Then UserValidationError."""
        # Arrange
        too_long_id = "a" * (USER_ID_MAX_LENGTH + 1)

        # Act / Assert
        with pytest.raises(UserValidationError) as exc_info:
            User.create(user_id=too_long_id, display_name="Learner")

        assert exc_info.value.code == "INVALID_USER_ID"


class TestDisplayNameValidation:
    """Tests for display_name invariant."""

    def test_display_name_empty_raises(self) -> None:
        """Given empty display_name, When User.create, Then UserValidationError."""
        # Arrange / Act / Assert
        with pytest.raises(UserValidationError) as exc_info:
            User.create(user_id="u1", display_name="")

        assert exc_info.value.code == "INVALID_DISPLAY_NAME"

    def test_display_name_whitespace_only_raises(self) -> None:
        """Given whitespace display_name, When User.create, Then UserValidationError."""
        # Arrange / Act / Assert
        with pytest.raises(UserValidationError) as exc_info:
            User.create(user_id="u1", display_name="  \t  ")

        assert exc_info.value.code == "INVALID_DISPLAY_NAME"

    def test_display_name_exceeds_max_length_raises(self) -> None:
        """Given too long display_name, When User.create, Then UserValidationError."""
        # Arrange
        too_long_name = "n" * (DISPLAY_NAME_MAX_LENGTH + 1)

        # Act / Assert
        with pytest.raises(UserValidationError) as exc_info:
            User.create(user_id="u1", display_name=too_long_name)

        assert exc_info.value.code == "INVALID_DISPLAY_NAME"
