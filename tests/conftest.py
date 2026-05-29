"""Shared pytest fixtures for Dual-Track RED skeleton (G0~G3 placeholders).

Grid literals are defined in Report/09 STEP 4 and Report/02 FIX-MAGIC / DT-*.
Uncomment and wire when Green phase begins.
"""

from __future__ import annotations

import os

import pytest

# import pytest

# G0 — FIX-MAGIC (complete 4×4 magic square)
# G0: list[list[int]] = [
#     [16, 3, 2, 13],
#     [5, 10, 11, 8],
#     [9, 6, 7, 12],
#     [4, 15, 14, 1],
# ]

# G1 — v0.2 placeholder: blanks (2,2),(3,3); missing {7,10}; expect [2,2,7,3,3,10]
# G1: list[list[int]] = [
#     [16, 3, 2, 13],
#     [5, 0, 11, 8],
#     [9, 6, 0, 12],
#     [4, 15, 14, 1],
# ]

# G2 — DT-06: blanks (1,1),(4,4); expect [1,1,16,4,4,1] (TBD until Green)
# G2: list[list[int]] = [
#     [0, 3, 2, 13],
#     [5, 10, 11, 8],
#     [9, 6, 7, 12],
#     [4, 15, 14, 0],
# ]

# G3 — DT-10: unsolvable partial grid (TBD literal)
# G3: list[list[int]] = ...  # placeholder

# @pytest.fixture(scope="module")
# def grid_g0() -> list[list[int]]:
#     return G0

# @pytest.fixture(scope="module")
# def grid_g1() -> list[list[int]]:
#     return G1

# @pytest.fixture(scope="module")
# def grid_g2() -> list[list[int]]:
#     return G2

# @pytest.fixture(scope="module")
# def grid_g3() -> list[list[int]]:
#     return G3


def pytest_configure(config: pytest.Config) -> None:
    """Register custom markers used by Golden Master regression tests."""
    config.addinivalue_line(
        "markers",
        "golden_master: Golden Master / approval regression tests (GM-TC-*)",
    )


@pytest.fixture
def golden_master_update() -> bool:
    """True when GOLDEN_MASTER_UPDATE requests baseline refresh."""
    return os.environ.get("GOLDEN_MASTER_UPDATE", "").lower() in {
        "1",
        "true",
        "yes",
    }
