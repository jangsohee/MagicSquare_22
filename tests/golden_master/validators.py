"""Golden Master contract validators for solver output."""

from __future__ import annotations

from magicsquare.boundary.schemas import (
    ERR_DUPLICATE_CODE,
    ERR_EMPTY_COUNT_CODE,
    ERR_EMPTY_COUNT_MESSAGE,
    ERR_NO_SOLUTION_CODE,
    ERR_NO_SOLUTION_MESSAGE,
    FailureResponse,
    SuccessResponse,
)
from magicsquare.entity.services.empty_cell_locator import find_blank_coords
from magicsquare.entity.services.magic_square_validator import is_magic_square
from magicsquare.entity.services.missing_number_finder import find_not_exist_nums
from magicsquare.entity.services.two_cell_solver import _filled_grid

from tests.golden_master.scenarios import AssignmentKind, GoldenMasterScenario

ERROR_ALIAS_TO_CONTRACT: dict[str, tuple[str, str]] = {
    "INVALID_BLANK_COUNT": (ERR_EMPTY_COUNT_CODE, ERR_EMPTY_COUNT_MESSAGE),
    "DUPLICATE_NUMBER": (ERR_DUPLICATE_CODE, "Duplicate non-zero value: 5."),
    "NO_VALID_MAGIC_SQUARE": (ERR_NO_SOLUTION_CODE, ERR_NO_SOLUTION_MESSAGE),
}


def validate_success_result(result: list[int], grid: list[list[int]]) -> None:
    """Assert int[6] format, 1-index coords, and row-major blank order."""
    assert len(result) == 6, "result must be int[6]"
    r1, c1, n1, r2, c2, n2 = result
    assert all(1 <= coordinate <= 4 for coordinate in (r1, c1, r2, c2)), (
        "coordinates must be 1-index in range 1..4"
    )
    assert all(1 <= value <= 16 for value in (n1, n2)), (
        "placed values must be in range 1..16"
    )

    blanks = find_blank_coords(grid)
    assert len(blanks) == 2, "grid must contain exactly two blanks for success"
    assert (r1, c1) == blanks[0], "first blank must follow row-major order"
    assert (r2, c2) == blanks[1], "second blank must follow row-major order"


def validate_assignment_kind(
    result: list[int],
    grid: list[list[int]],
    assignment_kind: AssignmentKind,
) -> None:
    """Assert forward-first or reverse-fallback assignment rules."""
    if assignment_kind == "error":
        return

    (r1, c1), (r2, c2) = find_blank_coords(grid)
    n_small, n_large = find_not_exist_nums(grid)
    forward = [r1, c1, n_small, r2, c2, n_large]
    reverse = [r1, c1, n_large, r2, c2, n_small]

    forward_grid = _filled_grid(grid, r1, c1, n_small, r2, c2, n_large)
    reverse_grid = _filled_grid(grid, r1, c1, n_large, r2, c2, n_small)
    forward_magic = is_magic_square(forward_grid)
    reverse_magic = is_magic_square(reverse_grid)

    assert result == forward or result == reverse, (
        "result must match forward or reverse assignment tuple"
    )
    assert is_magic_square(
        _filled_grid(grid, r1, c1, result[2], r2, c2, result[5])
    ), "result must complete a magic square"

    if assignment_kind == "success":
        expected = forward if forward_magic else reverse
        assert forward_magic or reverse_magic, "at least one assignment must succeed"
        assert result == expected, (
            "expected small-first assignment when forward succeeds, "
            "otherwise reverse fallback"
        )
    elif assignment_kind == "reverse":
        assert not forward_magic, "forward assignment must fail before reverse fallback"
        assert reverse_magic, "reverse assignment must succeed for this scenario"
        assert result == reverse, "expected reverse (large-at-first-blank) assignment"


def validate_error_response(
    response: FailureResponse,
    error_alias: str,
) -> None:
    """Assert Boundary error contract code and message."""
    expected_code, expected_message = ERROR_ALIAS_TO_CONTRACT[error_alias]
    assert response["status"] == "ERROR"
    assert response["code"] == expected_code
    assert response["message"] == expected_message


def validate_scenario_response(
    scenario: GoldenMasterScenario,
    response: SuccessResponse | FailureResponse,
) -> None:
    """Validate solver response against Golden Master contract rules."""
    if scenario.assignment_kind == "error":
        assert scenario.error_alias is not None
        validate_error_response(response, scenario.error_alias)
        return

    assert response["status"] == "OK"
    validate_success_result(response["result"], scenario.grid)
    validate_assignment_kind(
        response["result"],
        scenario.grid,
        scenario.assignment_kind,
    )
