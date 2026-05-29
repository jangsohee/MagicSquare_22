"""Golden Master input scenarios for GM-TC-01~05 regression suite."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Literal

AssignmentKind = Literal["success", "reverse", "error"]


@dataclass(frozen=True, slots=True)
class GoldenMasterScenario:
    """One Golden Master scenario with TC-ID and section key."""

    tc_id: str
    section_name: str
    grid: list[list[int]]
    assignment_kind: AssignmentKind
    error_alias: str | None = None


GM_TC_01_NORMAL_SUCCESS: Final[GoldenMasterScenario] = GoldenMasterScenario(
    tc_id="GM-TC-01",
    section_name="normal_success",
    grid=[
        [16, 2, 3, 13],
        [5, 11, 10, 8],
        [9, 7, 0, 12],
        [4, 14, 15, 0],
    ],
    assignment_kind="success",
)

GM_TC_02_REVERSE_SUCCESS: Final[GoldenMasterScenario] = GoldenMasterScenario(
    tc_id="GM-TC-02",
    section_name="reverse_success",
    grid=[
        [0, 3, 2, 13],
        [5, 10, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 0],
    ],
    assignment_kind="reverse",
)

GM_TC_03_INVALID_BLANK_COUNT: Final[GoldenMasterScenario] = GoldenMasterScenario(
    tc_id="GM-TC-03",
    section_name="invalid_blank_count",
    grid=[
        [16, 3, 2, 13],
        [5, 10, 11, 8],
        [9, 6, 0, 12],
        [4, 15, 0, 0],
    ],
    assignment_kind="error",
    error_alias="INVALID_BLANK_COUNT",
)

GM_TC_04_DUPLICATE_NUMBER: Final[GoldenMasterScenario] = GoldenMasterScenario(
    tc_id="GM-TC-04",
    section_name="duplicate_number",
    grid=[
        [16, 3, 2, 0],
        [5, 10, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 5, 0],
    ],
    assignment_kind="error",
    error_alias="DUPLICATE_NUMBER",
)

GM_TC_05_NO_VALID_MAGIC_SQUARE: Final[GoldenMasterScenario] = GoldenMasterScenario(
    tc_id="GM-TC-05",
    section_name="no_valid_solution",
    grid=[
        [16, 0, 2, 13],
        [5, 10, 0, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 3],
    ],
    assignment_kind="error",
    error_alias="NO_VALID_MAGIC_SQUARE",
)

GOLDEN_MASTER_SCENARIOS: Final[tuple[GoldenMasterScenario, ...]] = (
    GM_TC_01_NORMAL_SUCCESS,
    GM_TC_02_REVERSE_SUCCESS,
    GM_TC_03_INVALID_BLANK_COUNT,
    GM_TC_04_DUPLICATE_NUMBER,
    GM_TC_05_NO_VALID_MAGIC_SQUARE,
)

SCENARIO_BY_SECTION: Final[dict[str, GoldenMasterScenario]] = {
    scenario.section_name: scenario for scenario in GOLDEN_MASTER_SCENARIOS
}
