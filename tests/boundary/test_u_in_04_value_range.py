"""Track A RED skeleton — U-IN-04 value range validation (E004).

AC-FR01-04 | cell ∉ {0}∪[1,16] → E004 / ERR_VALUE_RANGE.
Domain execute 0회 (U-FLOW-02 연계).
"""

from __future__ import annotations

import pytest

from magicsquare.boundary.input_validator import InputValidator


class TestUIn04ValueRange:
    """U-IN-04 | AC-FR01-04 — value range rejection before Domain entry."""

    def test_u_in_04a_cell_17_returns_e004(self) -> None:
        """U-IN-04a | cell=17 → E004."""
        # Given
        # matrix = [[16, 3, 2, 13], [5, 10, 11, 8], [9, 6, 7, 12], [4, 15, 14, 17]]
        # validator = InputValidator()

        # When
        # response = validator.validate(matrix)

        # Then — E004 Failure envelope; execute 0회
        pytest.fail("RED: U-IN-04a — cell=17 → E004 (AC-FR01-04)")

    def test_u_in_04b_cell_minus_one_returns_e004(self) -> None:
        """U-IN-04b | cell=-1 → E004."""
        # Given
        # matrix = [[16, 3, 2, 13], [5, -1, 11, 8], [9, 6, 7, 12], [4, 15, 14, 1]]
        # validator = InputValidator()

        # When
        # response = validator.validate(matrix)

        # Then — E004 Failure envelope; execute 0회
        pytest.fail("RED: U-IN-04b — cell=-1 → E004 (AC-FR01-04)")
