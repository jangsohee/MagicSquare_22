"""4×4 grid input panel for the Magic Square GUI."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QGridLayout,
    QGroupBox,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from magicsquare.entity.magic_constant import MagicConstant


class GridPanel(QGroupBox):
    """Editable 4×4 grid; ``0`` denotes an empty cell."""

    GRID_SIZE = MagicConstant.GRID_SIZE

    def __init__(self, parent: QWidget | None = None) -> None:
        """Build a labeled 4×4 spin-box grid."""
        super().__init__("4×4 격자 (0 = 빈칸)", parent)
        self._cells: list[list[QSpinBox]] = []
        self._build_layout()

    def _build_layout(self) -> None:
        """Lay out row/column spin boxes."""
        outer = QVBoxLayout(self)
        grid = QGridLayout()
        grid.setSpacing(6)

        for row in range(self.GRID_SIZE):
            row_cells: list[QSpinBox] = []
            for col in range(self.GRID_SIZE):
                spin = QSpinBox()
                spin.setRange(0, 16)
                spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
                spin.setMinimumWidth(52)
                spin.setSpecialValueText("·")
                grid.addWidget(spin, row, col)
                row_cells.append(spin)
            self._cells.append(row_cells)

        outer.addLayout(grid)

    def read_grid(self) -> list[list[int]]:
        """Return the current grid values as ``list[list[int]]``."""
        return [[cell.value() for cell in row] for row in self._cells]

    def set_grid(self, grid: list[list[int]]) -> None:
        """Populate spin boxes from a 4×4 grid."""
        for row_idx, row in enumerate(grid):
            for col_idx, value in enumerate(row):
                self._cells[row_idx][col_idx].setValue(value)

    def clear_grid(self) -> None:
        """Reset all cells to empty (0)."""
        for row in self._cells:
            for cell in row:
                cell.setValue(0)

    def clear_highlights(self) -> None:
        """Remove solution highlight styling from all cells."""
        for row in self._cells:
            for cell in row:
                cell.setStyleSheet("")

    def apply_solution_tuple(self, result: list[int]) -> None:
        """Apply ``int[6]`` = ``[r1,c1,n1,r2,c2,n2]`` to the grid (1-index)."""
        if len(result) != 6:
            msg = f"Solution tuple must have 6 elements, got {len(result)}"
            raise ValueError(msg)
        r1, c1, n1, r2, c2, n2 = result
        self.highlight_solution(r1, c1, n1, r2, c2, n2)

    def highlight_solution(
        self,
        r1: int,
        c1: int,
        n1: int,
        r2: int,
        c2: int,
        n2: int,
    ) -> None:
        """Highlight solution coordinates (1-index) and show assigned values."""
        self.clear_highlights()
        placements = ((r1, c1, n1), (r2, c2, n2))
        for row, col, value in placements:
            cell = self._cells[row - 1][col - 1]
            cell.setValue(value)
            cell.setStyleSheet(
                "QSpinBox { background-color: #d4edda; font-weight: bold; }"
            )
