"""Application entry point for the PyQt GUI."""

from __future__ import annotations

import logging
import sys

from PyQt6.QtWidgets import QApplication

from magicsquare.boundary.gui.main_window import MainWindow

logger = logging.getLogger(__name__)


def main() -> int:
    """Launch the Magic Square GUI application.

    Returns:
        Process exit code from ``QApplication.exec()``.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )
    app = QApplication(sys.argv)
    app.setApplicationName("MagicSquare")
    window = MainWindow()
    window.show()
    logger.info("Magic Square GUI started")
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
