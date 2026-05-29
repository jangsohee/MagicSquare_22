"""Offscreen PyQt tests for ``MainWindow`` (Report/16 REFACTOR ②)."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from magicsquare.boundary.example_grids import UT09_PARTIAL_GRID, UT09_PARTIAL_RESULT
from magicsquare.boundary.gui.main_window import MainWindow
from magicsquare.boundary.schemas import (
    ERR_NULL_GRID_CODE,
    ERR_NULL_GRID_MESSAGE,
)


@pytest.fixture
def main_window(qapp: object) -> MainWindow:
    """Main window with mocked boundary (injected per test)."""
    _ = qapp
    return MainWindow(boundary=MagicMock(), example_grid=UT09_PARTIAL_GRID)


class TestMainWindowSolve:
    """GUI routes Boundary envelopes only (no broad ``except Exception``)."""

    def test_solve_ok_shows_ok_status_and_result_text(
        self, main_window: MainWindow
    ) -> None:
        """OK envelope → status label and result panel."""
        main_window._boundary.solve.return_value = {
            "status": "OK",
            "result": UT09_PARTIAL_RESULT,
        }
        main_window._load_example()

        main_window._on_solve()

        assert "OK" in main_window._status_label.text()
        assert "result =" in main_window._result_view.toPlainText()

    def test_solve_error_shows_error_code_and_message(
        self, main_window: MainWindow
    ) -> None:
        """ERROR envelope → code in status, message in panel."""
        main_window._boundary.solve.return_value = {
            "status": "ERROR",
            "code": ERR_NULL_GRID_CODE,
            "message": ERR_NULL_GRID_MESSAGE,
        }
        main_window._load_example()

        main_window._on_solve()

        assert ERR_NULL_GRID_CODE in main_window._status_label.text()
        assert main_window._result_view.toPlainText() == ERR_NULL_GRID_MESSAGE

    def test_boundary_exception_propagates_without_gui_swallow(
        self, main_window: MainWindow
    ) -> None:
        """Unexpected errors are not caught — envelope-only routing."""
        main_window._boundary.solve.side_effect = RuntimeError("boom")
        main_window._load_example()

        with pytest.raises(RuntimeError, match="boom"):
            main_window._on_solve()
