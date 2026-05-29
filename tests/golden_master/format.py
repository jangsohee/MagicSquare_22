"""Golden Master baseline text format helpers."""

from __future__ import annotations

import re
from typing import Final

from magicsquare.boundary.schemas import FailureResponse, SuccessResponse

SECTION_SEPARATOR: Final[str] = "________________________________________"

SECTION_HEADER_PATTERN: Final[re.Pattern[str]] = re.compile(r"^\[(?P<name>[a-z_]+)\]$")


def grid_to_input_lines(grid: list[list[int]]) -> list[str]:
    """Render a 4x4 grid as space-separated row lines."""
    return [" ".join(str(cell) for cell in row) for row in grid]


def format_result_list(result: list[int]) -> str:
    """Render solver result tuple without spaces after commas."""
    return "[" + ",".join(str(value) for value in result) + "]"


def response_to_section(
    name: str,
    grid: list[list[int]],
    response: SuccessResponse | FailureResponse,
) -> str:
    """Serialize one scenario block for the golden master baseline file."""
    lines = [f"[{name}]", "Input:"]
    lines.extend(grid_to_input_lines(grid))
    if response["status"] == "OK":
        lines.extend(["Output:", format_result_list(response["result"])])
    else:
        lines.extend(["Error:", response["code"]])
    return "\n".join(lines)


def build_golden_master_document(
    sections: list[str],
) -> str:
    """Join scenario sections with the canonical separator."""
    body = f"\n{SECTION_SEPARATOR}\n\n".join(sections)
    return f"{body}\n"


def parse_golden_master_document(text: str) -> dict[str, str]:
    """Parse a golden master file into scenario-name → section text."""
    chunks = re.split(
        rf"\n{re.escape(SECTION_SEPARATOR)}\n\n",
        text.strip(),
    )
    parsed: dict[str, str] = {}
    for chunk in chunks:
        if not chunk.strip():
            continue
        header_match = SECTION_HEADER_PATTERN.match(chunk.splitlines()[0])
        if header_match is None:
            msg = f"Invalid golden master section header: {chunk.splitlines()[0]!r}"
            raise ValueError(msg)
        parsed[header_match.group("name")] = chunk.strip()
    return parsed
