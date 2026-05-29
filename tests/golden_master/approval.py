"""Approve-pattern helper for Golden Master regression tests."""

from __future__ import annotations

import difflib
from pathlib import Path

from tests.golden_master.builder import build_golden_master_baseline
from tests.golden_master.format import parse_golden_master_document

DIFF_FROMFILE = "expected"
DIFF_TOFILE = "actual"


def _normalize(text: str) -> str:
    """Normalize line endings and trailing newline."""
    return text.replace("\r\n", "\n").strip() + "\n"


def format_diff(expected: str, actual: str) -> str:
    """Render unified diff with ``--- expected`` / ``+++ actual`` headers."""
    return "".join(
        difflib.unified_diff(
            expected.splitlines(keepends=True),
            actual.splitlines(keepends=True),
            fromfile=DIFF_FROMFILE,
            tofile=DIFF_TOFILE,
        )
    )


def approve(
    actual: str,
    expected_path: Path,
    *,
    update: bool = False,
) -> None:
    """Compare full golden master document against the baseline file.

    When ``expected_path`` is missing or ``update`` is True, write ``actual``
    to the file. Otherwise compare line-by-line and fail with a unified diff.

    Args:
        actual: Serialized golden master document from the current run.
        expected_path: Path to the committed baseline file.
        update: When True, overwrite the baseline with ``actual``.

    Raises:
        AssertionError: When the baseline exists and differs from ``actual``.
    """
    normalized_actual = _normalize(actual)

    if update or not expected_path.is_file():
        expected_path.parent.mkdir(parents=True, exist_ok=True)
        expected_path.write_text(normalized_actual, encoding="utf-8", newline="\n")
        return

    expected = _normalize(expected_path.read_text(encoding="utf-8"))
    if expected == normalized_actual:
        return

    diff_text = format_diff(expected, normalized_actual)
    msg = (
        f"Golden master mismatch for {expected_path.name}.\n"
        f"Set GOLDEN_MASTER_UPDATE=1 or run scripts/generate_golden_master.py "
        f"to refresh the baseline.\n\n{diff_text}"
    )
    raise AssertionError(msg)


def approve_section(
    actual_section: str,
    expected_path: Path,
    section_name: str,
    *,
    update: bool = False,
) -> None:
    """Compare one scenario section against the golden master baseline.

    If the baseline file is missing, bootstrap the full document from live
    solver output. When ``update`` is True, refresh the entire baseline file.

    Args:
        actual_section: Serialized section text for the current scenario.
        expected_path: Path to ``golden_master_expected.txt``.
        section_name: Section key such as ``normal_success``.
        update: When True, regenerate the full baseline file.

    Raises:
        AssertionError: When the section differs from the baseline.
    """
    normalized_actual = _normalize(actual_section)

    if update:
        approve(build_golden_master_baseline(), expected_path, update=True)
        return

    if not expected_path.is_file():
        approve(build_golden_master_baseline(), expected_path, update=False)
        return

    sections = parse_golden_master_document(
        expected_path.read_text(encoding="utf-8")
    )
    expected_section = _normalize(sections[section_name])

    if expected_section == normalized_actual:
        return

    diff_text = format_diff(expected_section, normalized_actual)
    msg = (
        f"Golden master mismatch for section [{section_name}] "
        f"in {expected_path.name}.\n"
        f"Set GOLDEN_MASTER_UPDATE=1 or run scripts/generate_golden_master.py "
        f"to refresh the baseline.\n\n{diff_text}"
    )
    raise AssertionError(msg)
