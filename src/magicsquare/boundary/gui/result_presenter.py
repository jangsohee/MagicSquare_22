"""Format and apply ``int[6]`` solution tuples for the GUI."""

from __future__ import annotations

from magicsquare.boundary.gui.grid_panel import GridPanel

SolutionTuple = tuple[int, int, int, int, int, int]


def parse_solution_tuple(result: list[int]) -> SolutionTuple:
    """Validate and unpack a six-element solution tuple.

    Args:
        result: Domain output ``[r1, c1, n1, r2, c2, n2]`` (1-index).

    Returns:
        Parsed coordinates and values.

    Raises:
        ValueError: When ``result`` does not have exactly six elements.
    """
    if len(result) != 6:
        msg = f"Solution tuple must have 6 elements, got {len(result)}"
        raise ValueError(msg)
    r1, c1, n1, r2, c2, n2 = result
    return r1, c1, n1, r2, c2, n2


def format_solution_text(result: list[int]) -> str:
    """Build human-readable text for the result panel."""
    r1, c1, n1, r2, c2, n2 = parse_solution_tuple(result)
    return (
        f"result = [{r1}, {c1}, {n1}, {r2}, {c2}, {n2}]\n"
        f"({r1},{c1}) ← {n1},  ({r2},{c2}) ← {n2}"
    )


class SolveResultPresenter:
    """Applies OK envelopes to grid highlights and result text."""

    def format_success_text(self, result: list[int]) -> str:
        """Return display text for a successful solve."""
        return format_solution_text(result)

    def apply_to_grid(self, panel: GridPanel, result: list[int]) -> None:
        """Highlight solution cells from an ``int[6]`` tuple."""
        panel.apply_solution_tuple(result)
