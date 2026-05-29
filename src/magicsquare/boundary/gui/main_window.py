"""Main window for the Magic Square PyQt application."""

from __future__ import annotations

import logging

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from magicsquare.boundary.example_grids import UT09_PARTIAL_GRID
from magicsquare.boundary.gui.grid_panel import GridPanel
from magicsquare.boundary.gui.result_presenter import SolveResultPresenter
from magicsquare.boundary.schemas import FailureResponse, SuccessResponse
from magicsquare.boundary.ui_boundary import UIBoundary
from magicsquare.entity.magic_constant import MagicConstant

logger = logging.getLogger(__name__)

_STYLE_READY = "color: #333;"
_STYLE_ERROR = "color: #b00020;"
_STYLE_OK = "color: #1b5e20;"


class MainWindow(QMainWindow):
    """Primary application window: grid input, solve, and result display."""

    def __init__(
        self,
        boundary: UIBoundary | None = None,
        example_grid: list[list[int]] | None = None,
        presenter: SolveResultPresenter | None = None,
    ) -> None:
        """Initialize window with optional boundary and example grid injection."""
        super().__init__()
        self._boundary = boundary or UIBoundary()
        self._presenter = presenter or SolveResultPresenter()
        self._example_grid = (
            [row[:] for row in example_grid]
            if example_grid is not None
            else [row[:] for row in UT09_PARTIAL_GRID]
        )
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

        self._build_intro(layout)
        layout.addWidget(self._grid_panel)
        self._build_button_row(layout)
        self._build_status_and_result(layout)
        self._wire_signals()

    def _build_intro(self, layout: QVBoxLayout) -> None:
        """Add introduction label."""
        intro = QLabel(
            f"부분 마방진을 완성합니다. 빈칸은 0, "
            f"완성 시 모든 선의 합 = {MagicConstant.TARGET_LINE_SUM}."
        )
        intro.setWordWrap(True)
        layout.addWidget(intro)

    def _build_button_row(self, layout: QVBoxLayout) -> None:
        """Add Solve / Clear / Load Example buttons."""
        button_row = QHBoxLayout()
        self._solve_button = QPushButton("Solve")
        self._clear_button = QPushButton("Clear")
        self._example_button = QPushButton("Load Example")
        button_row.addWidget(self._solve_button)
        button_row.addWidget(self._clear_button)
        button_row.addWidget(self._example_button)
        button_row.addStretch()
        layout.addLayout(button_row)

    def _build_status_and_result(self, layout: QVBoxLayout) -> None:
        """Add status label and read-only result panel."""
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

    def _wire_signals(self) -> None:
        """Connect button clicks to handlers."""
        self._solve_button.clicked.connect(self._on_solve)
        self._clear_button.clicked.connect(self._on_clear)
        self._example_button.clicked.connect(self._load_example)

    def _reset_ready_ui(self, message: str = "Ready") -> None:
        """Clear highlights, result text, and set neutral ready status."""
        self._grid_panel.clear_highlights()
        self._status_label.setText(message)
        self._status_label.setStyleSheet(_STYLE_READY)
        self._result_view.clear()

    def _load_example(self) -> None:
        """Fill the grid with the UT-09 example partial magic square."""
        self._grid_panel.set_grid(self._example_grid)
        self._reset_ready_ui("Ready — example grid loaded.")

    def _on_clear(self) -> None:
        """Reset grid and result display."""
        self._grid_panel.clear_grid()
        self._reset_ready_ui()

    def _on_solve(self) -> None:
        """Validate and solve the current grid via ``UIBoundary``."""
        grid = self._grid_panel.read_grid()
        logger.debug("Solve requested for grid=%s", grid)

        response = self._boundary.solve(grid)

        if response["status"] == "ERROR":
            self._show_failure(response)
            return
        self._show_success(response)

    def _show_failure(self, response: FailureResponse) -> None:
        """Display validation or domain failure envelope."""
        self._grid_panel.clear_highlights()
        self._status_label.setText(f"ERROR — {response['code']}")
        self._status_label.setStyleSheet(_STYLE_ERROR)
        self._result_view.setPlainText(response["message"])

    def _show_success(self, response: SuccessResponse) -> None:
        """Display OK envelope and highlight solution cells."""
        result = response["result"]
        self._presenter.apply_to_grid(self._grid_panel, result)
        self._status_label.setText("OK — magic square completion found")
        self._status_label.setStyleSheet(_STYLE_OK)
        self._result_view.setPlainText(self._presenter.format_success_text(result))
