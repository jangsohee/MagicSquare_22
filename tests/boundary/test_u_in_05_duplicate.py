"""Track A RED skeleton — U-IN-05 duplicate non-zero validation (E005).

AC-FR01-06 | non-zero 중복 → E005 / ERR_DUPLICATE.
"""

from __future__ import annotations

import pytest

from magicsquare.boundary.input_validator import InputValidator


class TestUIn05Duplicate:
    """U-IN-05 | AC-FR01-06 — duplicate non-zero rejection."""

    def test_u_in_05_duplicate_five_returns_e005(self) -> None:
        """U-IN-05 | non-zero duplicate 5 → E005."""
        # Given
        # matrix = [[16, 3, 2, 13], [5, 10, 11, 8], [9, 6, 7, 12], [4, 15, 5, 1]]
        # validator = InputValidator()

        # When
        # response = validator.validate(matrix)

        # Then — E005 Failure envelope; execute 0회
        pytest.fail("RED: U-IN-05 — non-zero duplicate 5 → E005 (AC-FR01-06)")
