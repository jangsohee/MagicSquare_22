# Golden Master Approval Pattern — GM-TC-01~05

## Purpose

Golden Master tests lock **observable solver output** for five representative scenarios.
Capture uses **API result serialization** (`UIBoundary.solve()` DTO → text section),
not GUI stdout.

Tag: `[TAG][GoldenMaster]` / `@pytest.mark.golden_master`

## Test cases

| TC-ID | Section | Scenario | Contract checks |
|-------|---------|----------|-----------------|
| GM-TC-01 | `normal_success` | Valid completion (small-first or fallback) | int[6], row-major, 1-index, assignment rule |
| GM-TC-02 | `reverse_success` | Forward fails, reverse succeeds | reverse fallback rule |
| GM-TC-03 | `invalid_blank_count` | Zero count ≠ 2 | `ERR_EMPTY_COUNT` (alias: INVALID_BLANK_COUNT) |
| GM-TC-04 | `duplicate_number` | Non-zero duplicate | `ERR_DUPLICATE` |
| GM-TC-05 | `no_valid_solution` | Domain unsolvable | `ERR_NO_SOLUTION` (alias: NO_VALID_MAGIC_SQUARE) |

## Approve pattern

Implementation: `tests/golden_master/approval.py`

| Condition | Behavior |
|-----------|----------|
| Baseline file **missing** | Bootstrap full document from live solver output |
| Baseline file **exists** | `open(expected).read()` vs serialized actual section |
| **Mismatch** | Unified diff with `--- expected` / `+++ actual` headers, then FAIL |
| Explicit refresh | `GOLDEN_MASTER_UPDATE=1` or `scripts/generate_golden_master.py` |

## Execution

```bash
# Run Golden Master suite only
pytest -m golden_master -v

# Refresh baseline after intentional output change
python scripts/generate_golden_master.py
# or
set GOLDEN_MASTER_UPDATE=1
pytest -m golden_master -v
```

## Example — passing run

```text
$ pytest -m golden_master -v
============================= test session starts =============================
collected 60 items / 54 deselected / 6 selected

tests/integration/test_golden_master_magic_square.py::TestGoldenMasterMagicSquare::test_gm_tc_01_normal_success PASSED
tests/integration/test_golden_master_magic_square.py::TestGoldenMasterMagicSquare::test_gm_tc_02_reverse_success PASSED
tests/integration/test_golden_master_magic_square.py::TestGoldenMasterMagicSquare::test_gm_tc_03_invalid_blank_count PASSED
tests/integration/test_golden_master_magic_square.py::TestGoldenMasterMagicSquare::test_gm_tc_04_duplicate_number PASSED
tests/integration/test_golden_master_magic_square.py::TestGoldenMasterMagicSquare::test_gm_tc_05_no_valid_magic_square PASSED
tests/integration/test_golden_master_magic_square.py::TestGoldenMasterMagicSquare::test_gm_tc_all_sections_match_full_baseline PASSED

====================== 6 passed, 54 deselected in 0.14s =======================
```

## Example — failure diff

```text
AssertionError: Golden master mismatch for section [normal_success] in golden_master_expected.txt.
Set GOLDEN_MASTER_UPDATE=1 or run scripts/generate_golden_master.py to refresh the baseline.

--- expected
+++ actual
@@ -5,7 +5,7 @@
 9 7 0 12
 4 14 15 0
 Output:
-[3,3,6,4,4,1]
+[9,9,9,9,9,9]
```

## Artifacts

| File | Role |
|------|------|
| `tests/integration/test_golden_master_magic_square.py` | GM-TC-01~05 + full-document check |
| `tests/golden_master_expected.txt` | Version-controlled baseline |
| `tests/golden_master/scenarios.py` | Input grids and TC metadata |
| `tests/golden_master/validators.py` | int[6] / row-major / assignment / error contract |
| `tests/golden_master/approval.py` | Approve helper and diff formatting |
| `scripts/generate_golden_master.py` | Baseline regeneration script |
