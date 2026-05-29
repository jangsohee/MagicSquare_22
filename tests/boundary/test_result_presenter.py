"""Tests for ``SolveResultPresenter`` and solution tuple formatting."""

from __future__ import annotations

import pytest

from magicsquare.boundary.example_grids import UT09_PARTIAL_RESULT
from magicsquare.boundary.gui.result_presenter import (
    format_solution_text,
    parse_solution_tuple,
)


class TestResultPresenter:
    """REFACTOR ③ — int[6] display formatting."""

    def test_format_solution_text_matches_ut09_tuple(self) -> None:
        """UT-09 result → stable multi-line display text."""
        text = format_solution_text(UT09_PARTIAL_RESULT)

        assert "result = [3, 3, 7, 4, 4, 1]" in text
        assert "(3,3) ← 7" in text

    def test_parse_solution_tuple_rejects_wrong_length(self) -> None:
        """Invalid length → ``ValueError``."""
        with pytest.raises(ValueError, match="6 elements"):
            parse_solution_tuple([1, 2, 3])
