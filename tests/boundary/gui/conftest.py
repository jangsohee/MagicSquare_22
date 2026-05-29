"""PyQt offscreen fixtures for GUI tests."""

from __future__ import annotations

import os

import pytest
from PyQt6.QtWidgets import QApplication


@pytest.fixture(scope="session", autouse=True)
def _qt_offscreen_platform() -> None:
    """Use offscreen platform so CI/headless runs do not require a display."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


@pytest.fixture(scope="module")
def qapp() -> QApplication:
    """Shared ``QApplication`` for widget tests."""
    instance = QApplication.instance()
    if instance is None:
        instance = QApplication([])
    return instance
