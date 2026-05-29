# Magic Square 프로젝트 — Golden Master 회귀 안전장치 보고서

**작성 목적:** GREEN 13/13 완료 후 **Refactoring 전 회귀 안전장치** 구축 — approve 패턴 · GM-TC-01~05 · baseline 버전 관리  
**대상:** 주니어 개발자 + Cursor AI 협업 학습 프로젝트  
**범위:** `golden_master_expected.txt` · GM-01~GM-10 · `test_golden_master_magic_square` · contract validators · README To-Do  
**선행 문서:** `Report/02-tdd-design-report.md`, `Report/14-green-completion-pyqt-gui-report.md`, `docs/golden_master_approval_design.md`, `README.md`  
**작성일:** 2026-05-29

---

## Executive Summary

Green 단계 완료 직후 Magic Square Solver 출력을 **Golden Master(Approval) 패턴**으로 고정했다. `UIBoundary.solve()` API DTO를 텍스트로 직렬화하고, `tests/golden_master_expected.txt`와 비교한다. baseline 없으면 bootstrap 생성, 불일치 시 `--- expected` / `+++ actual` unified diff 후 FAIL.

| 항목 | 결과 |
|------|------|
| **TDD phase** | GREEN 완료 → **REFACTOR 전 GM 구축** |
| **GM 체크리스트** | GM-01~GM-10 **전부 완료 ✅** |
| **테스트** | GM-TC-01~05 + full baseline = **6 passed** |
| **전체 suite** | **60 passed** (Golden Master 포함) |
| **실행** | `pytest -m golden_master -v` |
| **baseline** | `tests/golden_master_expected.txt` (git add 대상) |
| **README** | RED To-Do — Golden Master 회귀 안전장치 섹션 추가 |

**Transcript:** `Prompting/15-golden-master-regression-prompt.md`

---

## STEP 1 — GM-01~GM-10 체크리스트

### 1.1 기준 파일 생성

| ID | 항목 | 산출물 | 상태 |
|----|------|--------|------|
| GM-01 | `golden_master_expected.txt` 생성 | `tests/golden_master_expected.txt` | ✅ |
| GM-02 | 정상/역순/오류 시나리오 5건 | 5 sections | ✅ |
| GM-03 | git add baseline | `git add tests/golden_master_expected.txt` | ✅ |

### 1.2 테스트 코드

| ID | 항목 | 산출물 | 상태 |
|----|------|--------|------|
| GM-04 | `test_golden_master_magic_square` | `tests/integration/test_golden_master_magic_square.py` | ✅ |
| GM-05 | approve 패턴 | `tests/golden_master/approval.py` | ✅ |
| GM-06 | PASS 확인 | `pytest -m golden_master -v` → 6 passed | ✅ |

### 1.3 회귀 보호

| ID | 규칙 | 검증 위치 | 상태 |
|----|------|-----------|------|
| GM-07 | row-major 빈칸 순서 | `validators.validate_success_result` | ✅ |
| GM-08 | 1-index 좌표 | `validators.validate_success_result` | ✅ |
| GM-09 | reverse fallback | `validators.validate_assignment_kind` | ✅ |
| GM-10 | Error Contract | `validators.validate_error_response` | ✅ |

---

## STEP 2 — Approve 패턴 설계

### 2.1 캡처 방식

| 방식 | 채택 | 설명 |
|------|------|------|
| stdout capture | ❌ | GUI/CLI 출력은 계약 외 |
| **API result serialization** | ✅ | `UIBoundary.solve()` → TypedDict → text section |

### 2.2 Approve 흐름

```
solve(grid) → validate contract → serialize section
    ↓
expected_path exists?
    ├─ No  → bootstrap full baseline (write file)
    └─ Yes → open(expected).read() vs actual
              ├─ Match → PASS
              └─ Diff  → unified diff → FAIL
```

### 2.3 baseline 갱신

```powershell
python scripts/generate_golden_master.py
# 또는
set GOLDEN_MASTER_UPDATE=1
pytest -m golden_master -v
```

---

## STEP 3 — GM-TC-01~05 시나리오

| TC-ID | Section | 입력 요약 | 기대 출력 |
|-------|---------|-----------|-----------|
| GM-TC-01 | `normal_success` | blanks (3,3),(4,4) · missing {1,6} | `[3,3,6,4,4,1]` (reverse fallback) |
| GM-TC-02 | `reverse_success` | G2 · blanks (1,1),(4,4) | `[1,1,16,4,4,1]` |
| GM-TC-03 | `invalid_blank_count` | zero×3 | `ERR_EMPTY_COUNT` |
| GM-TC-04 | `duplicate_number` | duplicate 5 | `ERR_DUPLICATE` |
| GM-TC-05 | `no_valid_solution` | G3 unsolvable | `ERR_NO_SOLUTION` |

> Error alias `INVALID_BLANK_COUNT` / `NO_VALID_MAGIC_SQUARE`는 테스트 메타데이터명. 구현 code는 Report/02·`schemas.py` (`ERR_EMPTY_COUNT`, `ERR_NO_SOLUTION`).

### 3.1 baseline 예시 (GM-TC-01)

```text
[normal_success]
Input:
16 2 3 13
5 11 10 8
9 7 0 12
4 14 15 0
Output:
[3,3,6,4,4,1]
```

---

## STEP 4 — pytest 검증

### 4.1 Golden Master suite

```powershell
pytest -m golden_master -v
```

**결과 (2026-05-29):**

```
collected 60 items / 54 deselected / 6 selected
tests/integration/test_golden_master_magic_square.py ......  [100%]
6 passed, 54 deselected in 0.12s
```

| Test | TC | 결과 |
|------|-----|------|
| `test_gm_tc_01_normal_success` | GM-TC-01 | PASSED |
| `test_gm_tc_02_reverse_success` | GM-TC-02 | PASSED |
| `test_gm_tc_03_invalid_blank_count` | GM-TC-03 | PASSED |
| `test_gm_tc_04_duplicate_number` | GM-TC-04 | PASSED |
| `test_gm_tc_05_no_valid_magic_square` | GM-TC-05 | PASSED |
| `test_gm_tc_all_sections_match_full_baseline` | ALL | PASSED |

### 4.2 전체 suite

```powershell
pytest tests/ -q
```

**결과:** **60 passed**

---

## STEP 5 — 산출물·디렉터리

```
tests/
├── golden_master_expected.txt          # baseline (version control)
├── golden_master/
│   ├── scenarios.py                    # GM-TC grids + metadata
│   ├── format.py                       # serialize / parse
│   ├── approval.py                     # approve + diff
│   ├── builder.py                      # live solver runner
│   └── validators.py                   # contract checks
├── integration/
│   └── test_golden_master_magic_square.py
scripts/
└── generate_golden_master.py
docs/
└── golden_master_approval_design.md
```

### 5.1 pytest 마커

`pyproject.toml`:

```toml
markers = [
    "golden_master: Golden Master / approval regression tests (GM-TC-*)",
]
```

클래스/모듈: `@pytest.mark.golden_master` · docstring `[TAG][GoldenMaster]`

---

## STEP 6 — README 갱신

`README.md` **RED 단계 To-Do 리스트** 하단에 추가:

- ### Golden Master 회귀 안전장치
- #### 기준 파일 생성 (GM-01~03)
- #### 테스트 코드 (GM-04~06)
- #### 회귀 보호 (GM-07~10)

> Refactoring 시작 전 구축 · GREEN 완료 후 즉시 적용.

---

## STEP 7 — Report/02·REG 연계

| REG / Invariant | Golden Master 보호 |
|-----------------|-------------------|
| REG-01 int[6] format | GM-TC-01/02 output + validators |
| REG-02 Error message | GM-TC-03~05 + byte-exact boundary tests |
| REG-05 Refactor without test change | approve baseline lock |
| REG-06 Integration real Domain | `UIBoundary` E2E, Mock 금지 |
| INV row-major blanks | GM-07 |
| INV 1-index coords | GM-08 |
| FR-05 forward/reverse | GM-09 |

---

## 다음 단계

- [ ] REFACTOR 단계 시작 전 `pytest -m golden_master -v` CI gate 추가 (선택)
- [ ] 의도적 계약 변경 시 Report/02 갱신 → baseline refresh → diff review
- [ ] GUI 출력은 Golden Master 대상 외 유지 (Boundary DTO만 lock)

---

## 변경 이력

| 날짜 | 내용 |
|------|------|
| 2026-05-29 | GM-01~GM-10 구축 · GM-TC-01~05 · README To-Do · Report/15 · Prompting/15 Export |

---

## 부록 A — 생성·갱신 파일

| 경로 | 설명 |
|------|------|
| `Report/15-golden-master-regression-report.md` | 본 보고서 |
| `Prompting/15-golden-master-regression-prompt.md` | Transcript Export |
| `tests/golden_master_expected.txt` | Golden Master baseline |
| `tests/integration/test_golden_master_magic_square.py` | GM-TC regression tests |
| `docs/golden_master_approval_design.md` | Approve 패턴 설계 |
| `README.md` | RED To-Do Golden Master 섹션 |

## 부록 B — 관련 문서

| 문서 | 경로 |
|------|------|
| TDD 계약 SSOT | `Report/02-tdd-design-report.md` |
| GREEN 완료 | `Report/14-green-completion-pyqt-gui-report.md` |
| Approve 설계 | `docs/golden_master_approval_design.md` |
| 테스트 플랜 | `docs/test_plan.md` |
