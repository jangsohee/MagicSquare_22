"""Generate or refresh tests/golden_master_expected.txt from live solver output."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT))

from tests.golden_master.approval import approve  # noqa: E402
from tests.golden_master.builder import build_golden_master_baseline  # noqa: E402

EXPECTED_PATH = PROJECT_ROOT / "tests" / "golden_master_expected.txt"


def main() -> int:
    """Write the Golden Master baseline file from current solver output."""
    baseline = build_golden_master_baseline()
    approve(baseline, EXPECTED_PATH, update=True)
    print(f"Updated {EXPECTED_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
