"""Build Golden Master baseline text from live solver output."""

from __future__ import annotations

from magicsquare.boundary.schemas import FailureResponse, SuccessResponse
from magicsquare.boundary.ui_boundary import UIBoundary

from tests.golden_master.format import build_golden_master_document, response_to_section
from tests.golden_master.scenarios import GOLDEN_MASTER_SCENARIOS, GoldenMasterScenario


def serialize_scenario_output(
    scenario: GoldenMasterScenario,
    response: SuccessResponse | FailureResponse,
) -> str:
    """Serialize one scenario response for golden master comparison."""
    return response_to_section(scenario.section_name, scenario.grid, response)


def build_golden_master_baseline() -> str:
    """Run all GM-TC scenarios and serialize solver responses."""
    boundary = UIBoundary()
    sections: list[str] = []
    for scenario in GOLDEN_MASTER_SCENARIOS:
        response = boundary.solve([row[:] for row in scenario.grid])
        sections.append(serialize_scenario_output(scenario, response))
    return build_golden_master_document(sections)


def run_scenario(
    scenario: GoldenMasterScenario,
) -> tuple[SuccessResponse | FailureResponse, str]:
    """Execute one scenario and return API response plus serialized section."""
    response = UIBoundary().solve([row[:] for row in scenario.grid])
    return response, serialize_scenario_output(scenario, response)
