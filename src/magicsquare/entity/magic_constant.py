"""Entity value objects for magic square domain rules."""

from __future__ import annotations


class MagicConstant:
    """Single source for magic square line-sum target (NFR-08)."""

    TARGET_LINE_SUM: int = 34
