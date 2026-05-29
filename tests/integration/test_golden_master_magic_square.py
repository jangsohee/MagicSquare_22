"""GM-TC-01~05 Golden Master regression tests for Magic Square Solver.

[TAG][GoldenMaster]
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.golden_master.approval import approve_section
from tests.golden_master.builder import build_golden_master_baseline, run_scenario
from tests.golden_master.scenarios import (
    GM_TC_01_NORMAL_SUCCESS,
    GM_TC_02_REVERSE_SUCCESS,
    GM_TC_03_INVALID_BLANK_COUNT,
    GM_TC_04_DUPLICATE_NUMBER,
    GM_TC_05_NO_VALID_MAGIC_SQUARE,
    GoldenMasterScenario,
)
from tests.golden_master.validators import validate_scenario_response

EXPECTED_PATH = Path(__file__).resolve().parents[1] / "golden_master_expected.txt"

pytestmark = pytest.mark.golden_master


def _assert_golden_master_scenario(
    scenario: GoldenMasterScenario,
    golden_master_update: bool,
) -> None:
    """Run one GM-TC scenario, validate contract, and approve serialized output."""
    # Given
    response, actual_section = run_scenario(scenario)

    # When / Then — contract rules
    validate_scenario_response(scenario, response)

    # Then — approve pattern (open(expected).read() vs actual)
    approve_section(
        actual_section,
        EXPECTED_PATH,
        scenario.section_name,
        update=golden_master_update,
    )


class TestGoldenMasterMagicSquare:
    """[TAG][GoldenMaster] GM-TC-01~05 solver output regression suite."""

    def test_gm_tc_01_normal_success(
        self,
        golden_master_update: bool,
    ) -> None:
        """GM-TC-01 | 정상 조합 성공 — int[6], row-major, small-first fallback."""
        _assert_golden_master_scenario(GM_TC_01_NORMAL_SUCCESS, golden_master_update)

    def test_gm_tc_02_reverse_success(
        self,
        golden_master_update: bool,
    ) -> None:
        """GM-TC-02 | reverse 조합 성공 — forward fails, reverse fallback."""
        _assert_golden_master_scenario(GM_TC_02_REVERSE_SUCCESS, golden_master_update)

    def test_gm_tc_03_invalid_blank_count(
        self,
        golden_master_update: bool,
    ) -> None:
        """GM-TC-03 | INVALID_BLANK_COUNT — ERR_EMPTY_COUNT error contract."""
        _assert_golden_master_scenario(
            GM_TC_03_INVALID_BLANK_COUNT,
            golden_master_update,
        )

    def test_gm_tc_04_duplicate_number(
        self,
        golden_master_update: bool,
    ) -> None:
        """GM-TC-04 | DUPLICATE_NUMBER — ERR_DUPLICATE error contract."""
        _assert_golden_master_scenario(GM_TC_04_DUPLICATE_NUMBER, golden_master_update)

    def test_gm_tc_05_no_valid_magic_square(
        self,
        golden_master_update: bool,
    ) -> None:
        """GM-TC-05 | NO_VALID_MAGIC_SQUARE — ERR_NO_SOLUTION error contract."""
        _assert_golden_master_scenario(
            GM_TC_05_NO_VALID_MAGIC_SQUARE,
            golden_master_update,
        )

    def test_gm_tc_all_sections_match_full_baseline(
        self,
        golden_master_update: bool,
    ) -> None:
        """GM-TC-ALL | Full golden_master_expected.txt document parity check."""
        from tests.golden_master.approval import approve

        actual = build_golden_master_baseline()
        approve(actual, EXPECTED_PATH, update=golden_master_update)
