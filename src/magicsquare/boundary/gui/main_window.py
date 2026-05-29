"""Main window for the Magic Square PyQt application."""

from __future__ import annotations

import logging

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from magicsquare.boundary.gui.grid_panel import GridPanel
from magicsquare.boundary.schemas import FailureResponse, SuccessResponse
from magicsquare.boundary.ui_boundary import UIBoundary
from magicsquare.entity.magic_constant import MagicConstant

logger = logging.getLogger(__name__)

# UT-09 / DT-03 example partial grid
EXAMPLE_GRID: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 0],
]


class MainWindow(QMainWindow):
    """Primary application window: grid input, solve, and result display."""

    def __init__(self, boundary: UIBoundary | None = None) -> None:
        """Initialize window with optional boundary injection for testing."""
        super().__init__()
        self._boundary = boundary or UIBoundary()
        self._grid_panel = GridPanel()
        self._result_view = QTextEdit()
        self._status_label = QLabel()
        self._build_ui()
        self._load_example()

    def _build_ui(self) -> None:
        """Assemble widgets and connect signals."""
        self.setWindowTitle("Magic Square 4×4")
        self.setMinimumSize(520, 560)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(12)

        intro = QLabel(
            f"부분 마방진을 완성합니다. 빈칸은 0, "
            f"완성 시 모든 선의 합 = {MagicConstant.TARGET_LINE_SUM}."
        )
        intro.setWordWrap(True)
        layout.addWidget(intro)
        layout.addWidget(self._grid_panel)

        button_row = QHBoxLayout()
        self._solve_button = QPushButton("Solve")
        self._clear_button = QPushButton("Clear")
        self._example_button = QPushButton("Load Example")
        button_row.addWidget(self._solve_button)
        button_row.addWidget(self._clear_button)
        button_row.addWidget(self._example_button)
        button_row.addStretch()
        layout.addLayout(button_row)

        self._status_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        status_font = QFont()
        status_font.setPointSize(10)
        status_font.setBold(True)
        self._status_label.setFont(status_font)
        layout.addWidget(self._status_label)

        self._result_view.setReadOnly(True)
        self._result_view.setMaximumHeight(120)
        self._result_view.setPlaceholderText("Solve 결과가 여기에 표시됩니다.")
        layout.addWidget(self._result_view)

        self._solve_button.clicked.connect(self._on_solve)
        self._clear_button.clicked.connect(self._on_clear)
        self._example_button.clicked.connect(self._load_example)

    def _load_example(self) -> None:
        """Fill the grid with the UT-09 example partial magic square."""
        self._grid_panel.set_grid(EXAMPLE_GRID)
        self._grid_panel.clear_highlights()
        self._status_label.setText("Ready — example grid loaded.")
        self._status_label.setStyleSheet("color: #333;")
        self._result_view.clear()

    def _on_clear(self) -> None:
        """Reset grid and result display."""
        self._grid_panel.clear_grid()
        self._grid_panel.clear_highlights()
        self._status_label.setText("Ready")
        self._status_label.setStyleSheet("color: #333;")
        self._result_view.clear()

    def _on_solve(self) -> None:
        """Validate and solve the current grid via ``UIBoundary``."""
        grid = self._grid_panel.read_grid()
        logger.debug("Solve requested for grid=%s", grid)

        try:
            response = self._boundary.solve(grid)
        except Exception as exc:  # noqa: BLE001 — show unexpected errors in GUI
            logger.exception("Unexpected error during solve")
            self._show_unexpected_error(str(exc))
            return

        if response["status"] == "ERROR":
            self._show_failure(response)
            return
        self._show_success(response)

    def _show_failure(self, response: FailureResponse) -> None:
        """Display validation or domain failure envelope."""
        self._grid_panel.clear_highlights()
        self._status_label.setText(f"ERROR — {response['code']}")
        self._status_label.setStyleSheet("color: #b00020;")
        self._result_view.setPlainText(response["message"])

    def _show_success(self, response: SuccessResponse) -> None:
        """Display OK envelope and highlight solution cells."""
        result = response["result"]
        r1, c1, n1, r2, c2, n2 = result
        self._grid_panel.highlight_solution(r1, c1, n1, r2, c2, n2)
        self._status_label.setText("OK — magic square completion found")
        self._status_label.setStyleSheet("color: #1b5e20;")
        self._result_view.setPlainText(
            f"result = [{r1}, {c1}, {n1}, {r2}, {c2}, {n2}]\n"
            f"({r1},{c1}) ← {n1},  ({r2},{c2}) ← {n2}"
        )

    def _show_unexpected_error(self, detail: str) -> None:
        """Show a modal for unexpected runtime failures."""
        self._grid_panel.clear_highlights()
        self._status_label.setText("ERROR — unexpected")
        self._status_label.setStyleSheet("color: #b00020;")
        self._result_view.setPlainText(detail)
        QMessageBox.critical(
            self,
            "Unexpected Error",
            "An unexpected error occurred. See the result panel for details.",
        )
