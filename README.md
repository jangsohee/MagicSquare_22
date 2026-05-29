# MagicSquare_

4×4 마방진을 다루는 학습·실험 프로젝트입니다.  
Cursor AI와 협업하며 **문제 정의 → 규칙 고정 → PRD → 검증 가능한 구현** 순서로 개발 역량을 기릅니다.

> **현재 단계:** **GREEN 6/13** (A-01~A-06 ✅) · boundary **20 passed** · [GREEN To-Do](#green-단계-to-do-리스트) · Report/13

---

## 프로젝트 한 줄 요약

4×4 격자에 숫자를 배치할 때, **‘완성’이 무엇인지**·**‘지금 상태가 규칙을 어기는지’**를 사람이 반복 계산하지 않고도 즉시·일관되게 알 수 있어야 합니다.  
이 프로젝트는 그 판단 기준을 먼저 고정하고, 작은 단위로 검증 가능한 형태로 쌓아 올리며, AI 도구와 협업해 **최소한의 피드백 루프**를 경험하는 것을 목표로 합니다.

---

## 왜 이 프로젝트인가

| 관점 | 내용 |
|------|------|
| **학습** | 주니어 개발자가 실제로 동작하는 소프트웨어를 만들며 역량을 쌓음 |
| **도구** | Cursor AI를 코드 생성기가 아닌 **협업 도구**로 활용 |
| **도메인** | 규칙이 명확하고(행·열·대각 합), 검증·테스트에 유리한 4×4 격자 문제 |
| **방법** | The Mom Test, 5 Whys, Dual-Track TDD(규칙을 먼저 고정) |

---

## 핵심 Invariant

주어진 4×4 배치에서 **“완성”**으로 인정되려면:

1. 정해진 숫자 집합(1~16)이 **중복·누락 없이** 한 번씩 사용된다.
2. **빈 칸이 없다.**
3. 모든 **행·열·대각선**의 합이 **동일**하다 (4×4·1~16 설정에서 **34**).

부분 완성 상태에서는 **위반은 즉시 드러내고**, 아직 판단할 수 없는 조건은 **“미정”**으로 둡니다.

---

## 표면 목표 vs 진짜 문제

| | 정의 |
|---|------|
| **표면 (피해야 할 정의)** | “4×4 마방진을 자동으로 만들고 검증하는 프로그램을 만든다.” |
| **진짜 문제** | 규칙 기반 **상태 판단**을 신뢰할 수 있게 만들고, 그 과정에서 **개발자로서의 사고**(불변 조건, 입출력 계약, 점진적 검증)를 훈련한다. |

---

## 훈련하려는 사고 능력

- 문제와 해결책 분리
- 불변 조건(invariant) 식별
- 입력·출력 계약을 말로 합의 가능하게 고정
- Dual-Track TDD (Boundary 계약 ∥ Domain 불변식)
- 가장 작은 참인 경우부터 점진적으로 신뢰 쌓기
- AI와 **검증 가능한 진술**을 공유하는 협업

---

## 프로젝트 구조

```
MagicSquare_/
├── .cursorrules                           # Cursor 전역 YAML 규칙 (요약)
├── .cursor/
│   ├── rules/                             # magicsquare-*.mdc (5개)
│   └── agents/                            # 역할별 Cursor Agent (8개)
├── docs/
│   ├── PRD_MagicSquare.md                 # 구현 전 PRD (v1.0 Draft)
│   └── test_plan.md                       # FR-01 / AC-FR01-01 테스트 계획
├── defect_list.md                         # 결함 DEF-001 부분 해소 · DEF-002~006 Open
├── README.md
├── pyproject.toml                         # pytest · pytest-cov · pydantic · black · ruff
├── .venv/                                 # 로컬 가상환경 (gitignore)
├── src/magicsquare/                       # Python ECB
│   ├── entity/                            # User Entity 구현됨
│   ├── boundary/                          # A-01 Green — entry · input_validator · schemas
│   ├── control/                           # (예정)
│   └── data/                              # (예정)
├── tests/
│   ├── conftest.py                        # G0~G3 placeholder (주석)
│   ├── entity/
│   │   ├── test_user.py                   # 9 passed
│   │   └── test_d_*.py                    # RED Skeleton — 수집 ERROR
│   ├── boundary/
│   │   ├── test_ac_fr01_01_null_grid.py   # UT-01 — 5 passed (A-01 Green)
│   │   └── test_u_*.py                    # Skeleton RED (3 failed) · ui_boundary 미구현 (2 errors)
│   └── data/ · integration/               # (예정)
├── Report/
│   ├── 01-problem-definition-report.md
│   ├── 02-tdd-design-report.md            # 계약·TC-ID SSOT
│   ├── 03-cursor-rules-and-implementation-report.md
│   ├── 04-magicsquare-rules-consolidation-report.md
│   ├── 05-cursor-agents-prompt-set-report.md
│   ├── 06-user-journey-to-scenario-verification-report.md
│   ├── 07-prd-creation-and-review-report.md
│   ├── 08-test-plan-red-phase-report.md   # test_plan · RED · QA
│   ├── 09-dual-track-red-design-report.md # FR-01~05 RED 설계표
│   ├── 10-dual-track-red-skeleton-report.md # RED Skeleton pytest 21건
│   ├── 11-coverage-html-qa-report.md      # htmlcov workaround · DEF-004
│   ├── 12-ac-fr01-01-green-phase-report.md # UT-01 Green · boundary 스켈레톤
│   └── 13-green-phase-readme-plan-report.md # GREEN 묶음 · README To-Do
└── Prompting/
    ├── 01-problem-definition-prompt.md
    ├── 02-tdd-design-prompt.md
    ├── 03-cursor-rules-implementation-prompt.md
    ├── 04-magicsquare-rules-consolidation-prompt.md
    ├── 05-cursor-agents-prompt-set-prompt.md
    ├── 06-user-journey-to-scenario-verification-prompt.md
    ├── 07-prd-creation-and-review-prompt.md
    ├── 08-test-plan-red-phase-prompt.md
    ├── 09-dual-track-red-design-prompt.md
    ├── 10-dual-track-red-skeleton-prompt.md
    ├── 11-coverage-html-qa-prompt.md
    ├── 12-ac-fr01-01-green-phase-prompt.md
    └── 13-green-phase-readme-plan-prompt.md
```

---

## 문서

### 핵심 (구현 착수 시)

| 문서 | 설명 |
|------|------|
| [**PRD**](docs/PRD_MagicSquare.md) | 구현 전 기준 — FR, BR, I/O·Error 계약, Dual-Track, Traceability |
| [**테스트 플랜**](docs/test_plan.md) | AC-FR01-01 앵커 · UT-01~08 · pytest-cov 전략 |
| [**결함 목록**](defect_list.md) | DEF-001 부분 해소 · DEF-002~006 Open |
| [TDD 설계 보고서](Report/02-tdd-design-report.md) | TC-ID·Error message·Invariant **단일 진실 원천** |
| [User Journey 보고서](Report/06-user-journey-to-scenario-verification-report.md) | Epic → Story → Scenario → Verification |
| [PRD 작성·검토 보고서](Report/07-prd-creation-and-review-report.md) | PRD 산출·7항목 검토·P0~P2 개선 권장 |
| [테스트 플랜·RED·QA 보고서](Report/08-test-plan-red-phase-report.md) | test_plan · boundary RED · defect_list · 커버리지 이슈 |
| [Dual-Track RED 설계 보고서](Report/09-dual-track-red-design-report.md) | U-IN/OUT/FLOW · D-LOC/MIS/VAL/SOL · G0~G3 · I1~I11 |
| [Dual-Track RED Skeleton 보고서](Report/10-dual-track-red-skeleton-report.md) | pytest 스켈레톤 21건 · conftest · RED 검증 |
| [커버리지 HTML QA 보고서](Report/11-coverage-html-qa-report.md) | htmlcov 생성 workaround · DEF-004 · Report/10 이후 |
| [AC-FR01-01 Green 보고서](Report/12-ac-fr01-01-green-phase-report.md) | UT-01 Green · boundary 최소 구현 |
| [GREEN 단계 README·묶음 계획](Report/13-green-phase-readme-plan-report.md) | RED/Green 묶음 · README To-Do · pytest 현황 |

### 설계·규칙·에이전트

| 문서 | 설명 |
|------|------|
| [문제 정의 보고서](Report/01-problem-definition-report.md) | Observation, Why #1~#3, 진짜 문제 정의 |
| [Cursor Rules·구현 보고서](Report/03-cursor-rules-and-implementation-report.md) | `.cursorrules` · User Entity |
| [Rules 5파일 통합 보고서](Report/04-magicsquare-rules-consolidation-report.md) | `magicsquare-*.mdc` 11→5 통합 |
| [Agent 프롬프트 세트 보고서](Report/05-cursor-agents-prompt-set-report.md) | `.cursor/agents/` 8종 |

### Transcript (Prompting)

| 문서 | 설명 |
|------|------|
| [01 문제 정의](Prompting/01-problem-definition-prompt.md) | |
| [02 TDD 설계](Prompting/02-tdd-design-prompt.md) | |
| [03 Cursor Rules·구현](Prompting/03-cursor-rules-implementation-prompt.md) | |
| [04 Rules 통합](Prompting/04-magicsquare-rules-consolidation-prompt.md) | |
| [05 Agent 세트](Prompting/05-cursor-agents-prompt-set-prompt.md) | |
| [06 User Journey](Prompting/06-user-journey-to-scenario-verification-prompt.md) | |
| [07 PRD 작성·검토](Prompting/07-prd-creation-and-review-prompt.md) | |
| [08 테스트 플랜·RED·QA](Prompting/08-test-plan-red-phase-prompt.md) | AC-FR01-01 · test_plan · boundary RED · defect_list |
| [09 Dual-Track RED 설계](Prompting/09-dual-track-red-design-prompt.md) | FR-01~05 RED 설계표 · Track A/B |
| [10 Dual-Track RED Skeleton](Prompting/10-dual-track-red-skeleton-prompt.md) | Report/09 → pytest Skeleton 21건 |
| [11 커버리지 HTML QA](Prompting/11-coverage-html-qa-prompt.md) | htmlcov 실패 진단 · workaround |
| [12 AC-FR01-01 Green](Prompting/12-ac-fr01-01-green-phase-prompt.md) | UT-01 Green · boundary 스켈레톤 |
| [13 GREEN README·묶음 계획](Prompting/13-green-phase-readme-plan-prompt.md) | RED/Green 묶음 · README To-Do Export |

### Cursor Rules

| 파일 | 설명 |
|------|------|
| [`.cursorrules`](.cursorrules) | project / architecture / tdd_rules 등 YAML 요약 |
| [`.cursor/rules/`](.cursor/rules/) | `magicsquare-project` · `forbidden` · `ecb-architecture` · `python-code-style` · `tdd-testing` |

**스택:** Python 3.10+ · PEP8 · type hints · pytest · ECB · Dual-Track TDD

---

## 고정 입출력 계약

| | 내용 |
|---|------|
| **입력** | `4×4 int[][]` — `0`=빈칸, 빈칸 정확히 2개, 값 `0` 또는 `1~16`, 0 제외 중복 금지 |
| **출력** | `int[6]` = `[r1,c1,n1,r2,c2,n2]` — 좌표 **1-index**, row-major 첫 빈칸 |
| **배치** | small-first → reverse; 둘 다 실패 시 `ERR_NO_SOLUTION` |
| **Magic Constant** | 10개 선 합 = **34** (`MagicConstant.TARGET_LINE_SUM`) |
| **Boundary 검증 순서** | `NULL → ROWS → COLS → RANGE → EMPTY_COUNT → DUPLICATE` |

상세: [PRD §12–13](docs/PRD_MagicSquare.md) · [TDD 설계 보고서](Report/02-tdd-design-report.md)

---

## 진행 상황

- [x] STEP 1~5 — 문제 정의 (Report/01)
- [x] Dual-Track TDD 설계 · 입출력 계약 (Report/02)
- [x] Cursor Rules — `.cursorrules` + `magicsquare-*.mdc` 5파일 (Report/03 → 04)
- [x] Cursor Agent 8종 (Report/05)
- [x] User Journey → Scenario → Verification (Report/06)
- [x] **PRD v1.0 Draft** · 7항목 검토 (Report/07, `docs/PRD_MagicSquare.md`)
- [x] `pyproject.toml` · User Entity (`tests/entity/` **9 passed**)
- [x] **테스트 플랜** (`docs/test_plan.md`, Report/08)
- [x] **UT-01 RED** — `tests/boundary/test_ac_fr01_01_null_grid.py` (5 tests)
- [x] **결함 목록** (`defect_list.md`, DEF-001~006)
- [x] **Dual-Track RED 설계표** (Report/09 — U-IN/OUT/FLOW, D-LOC/MIS/VAL/SOL)
- [x] **Dual-Track RED Skeleton** (Report/10 — 21 pytest 스켈레톤, G0~G3 placeholder)
- [x] **UT-01 Green (A-01)** — `src/magicsquare/boundary/` null 분기 (5 passed, Report/12)
- [x] **GREEN 묶음 계획 · README To-Do** (Report/13 — A/B/I 13묶음)
- [x] **A-02 Green** — UT-02 rows (`ERR_GRID_ROWS`, 4 passed)
- [x] **A-04 Green** — UT-04/05 value range (`ERR_VALUE_RANGE`, 3 passed)
- [x] **A-05 Green** — UT-06/07 empty count (`ERR_EMPTY_COUNT`, 3 passed)
- [x] **A-06 Green** — UT-08 duplicate (`ERR_DUPLICATE`, 2 passed)
- [ ] RED 테스트 ↔ PRD SSOT 정렬 (`INVALID_SIZE` vs `ERR_NULL_GRID` — DEF-002·003)
- [ ] DEC-01: ECB 레이어 배치 확정 (Report/02 ↔ PRD)
- [ ] PRD v1.1 (AC-ID Matrix, Layer 용어 통일)
- [ ] Mom Test · 1차 사용자 확정
- [ ] Track B 병렬: **B-01** D-VAL Green
- [ ] Track A 순차: **A-07~A-08** Green
- [ ] Data Track · 통합 테스트 (I-01 / I-02)

---

## pytest 현황 (2026-05-29)

| Suite | 결과 | 비고 |
|-------|------|------|
| `tests/boundary/test_ac_fr01_01_null_grid.py` | **5 passed** | A-01 Green ✅ |
| `tests/boundary/test_ut02_grid_rows.py` | **4 passed** | A-02 Green ✅ |
| `tests/boundary/test_u_in_04_value_range.py` | **3 passed** | A-04 Green ✅ |
| `tests/boundary/test_ut06_empty_count.py` | **3 passed** | A-05 Green ✅ |
| `tests/boundary/test_u_in_05_duplicate.py` | **2 passed** | A-06 Green ✅ |
| `tests/boundary/` (Green suite) | **20 passed** | A-01~A-06 ✅ |
| `tests/boundary/` (전체) | **20 passed, 2 errors** | U-FLOW/U-OUT collection ERROR |
| `tests/entity/test_user.py` | **9 passed** | User Entity Green |
| `tests/entity/test_d_*.py` | **4 errors** (수집) | `entity.services` 미구현 |

**다음 Green 착수:** [A-07](#a-07--u-flow-execute-isolation-fr-01) (순차) 또는 [B-01](#b-01--d-val-magic-validator-fr-04--dt-0108) (병렬)

---

## RED 단계 To-Do 리스트

> RED Skeleton 21건 + UT-01 Full RED. UT-01은 **Green 완료(A-01)** — 아래 UT-01 항목은 RED 작성 완료로 체크.
> Error code/message는 테스트 `INVALID_SIZE` vs PRD `ERR_NULL_GRID` **drift** (DEF-002) — SSOT 통일 전 Green 진행 중.

### Track A — UI / Boundary (P0: AC-FR01-01 / UT-01) — RED 작성 완료 ✅
- [x] TC-A-01: grid=None → status=`"ERROR"` *(A-01 Green)*
- [x] TC-A-02: code assert *(테스트: `INVALID_SIZE` — PRD drift DEF-002)*
- [x] TC-A-03: message byte-exact *(테스트: `Grid must be 4x4.`)*
- [x] TC-A-04: Domain `resolve` 0회 mock *(A-01 Green)*
- [x] TC-A-07: pydantic ERROR envelope *(A-01 Green)*

### Track A — P1 확장 (AC-FR01-02·03 / UT-02·03)
- [x] TC-A-05: `grid=[]` → `ERR_GRID_ROWS` *(A-02 Green)*
- [x] TC-A-06: 3×4 → `ERR_GRID_ROWS` *(A-02 Green)*
- [x] UT-02 RED — `test_ut02_grid_rows.py` ×4 *(A-02)*

- [x] UT-03 RED — `test_ut03_grid_cols.py` ×3 *(A-03)*

### Track A — P2 (Skeleton → Full RED 대기)
- [x] U-IN-04/05 value range — `test_u_in_04_value_range.py` *(A-04 Green)*
- [x] UT-06/07 empty count — `test_ut06_empty_count.py` *(A-05 Green)*
- [x] U-IN-05 duplicate — `test_u_in_05_duplicate.py` *(A-06 Green)*
- [ ] U-FLOW-02 E004/E005 — `test_u_flow_02_execute_isolation.py` *(A-07)*
- [ ] U-OUT-01~03 — `test_u_out_output_contract.py` *(A-08)*

### Track B — Domain Skeleton (Full RED 대기)
- [ ] D-VAL ×6 — `test_d_val.py` *(B-01)*
- [ ] D-LOC + D-MIS — `test_d_loc_01.py`, `test_d_mis_01.py` *(B-02)*
- [ ] D-SOL ×4 — `test_d_sol.py` *(B-03)*

### Track B — Domain / Logic 격리 (UT-01에서 null 커버)
- [x] TC-B-01~03: null 입력 Domain 미진입 *(A-01 `resolve` mock — DEF-003 drift: `resolve` vs `solve_partial_grid`)*
- [x] TC-B-04: AC-FR01-02~06 UT-01 RED 범위 외 확인

### 커버리지 목표
- [ ] Domain Logic: 95%+ (`pip install pytest-cov`)
- [ ] Boundary Layer: 85%+
- [ ] 전체 TOTAL: 80%+

### 결함 목록 연결
- [x] [defect_list.md](defect_list.md) 생성 및 발견 결함 기록 (DEF-001~006)
- [x] DEF-001 부분 해소 — `magicsquare.boundary` 존재 · UT-01 5 passed (A-01)
- [ ] DEF-002~006 해소 및 회귀 테스트 통과

---

## GREEN 단계 To-Do 리스트

> **RED 1묶음 = GREEN 1묶음** (커밋 단위). 상세: [Report/13](Report/13-green-phase-readme-plan-report.md).
> 검증 순서: `NULL → ROWS → COLS → RANGE → EMPTY_COUNT → DUPLICATE` ([Report/02](Report/02-tdd-design-report.md)).
> Track B(B-01~B-03)는 A-01 이후 **병렬** 가능. A-08·I-*는 선행 묶음 Green 완료 후.

**묶음 요약:** Track A 8 · Track B 3 · Integration 2 = **13 Green 묶음** (A-01~A-06 완료, **7 remaining**)

### Track A — Boundary (순차)

#### A-01 · UT-01 null grid (AC-FR01-01) ✅
- [x] RED: `test_ac_fr01_01_null_grid.py` (5 tests)
- [x] GREEN: `grid is None` → ERROR envelope + Domain early return
- [x] pytest: `python -m pytest tests/boundary/test_ac_fr01_01_null_grid.py -v` → **5 passed**
- [x] 커밋 예: `feat(boundary): AC-FR01-01 null grid Green (A-01)`

#### A-02 · UT-02 grid rows (AC-FR01-02) ✅
- [x] RED: `test_ut02_grid_rows.py` (4 tests)
- [x] GREEN: `len(grid) != 4` → `ERR_GRID_ROWS`
- [x] pytest: `python -m pytest tests/boundary/test_ut02_grid_rows.py -v` → **4 passed**
- [x] 커밋: `feat(boundary): AC-FR01-02 ERR_GRID_ROWS Green (A-02)`

#### A-03 · UT-03 grid cols (AC-FR01-03) ✅
- [x] RED: `test_ut03_grid_cols.py` (3 tests)
- [x] GREEN: `len(row) != 4` → `ERR_GRID_COLS`
- [x] pytest: `python -m pytest tests/boundary/test_ut03_grid_cols.py -v` → **3 passed**
- [x] 커밋: `feat(boundary): AC-FR01-03 ERR_GRID_COLS Green (A-03)`

#### A-04 · UT-04/05 value range (AC-FR01-04) ✅
- [x] RED: `test_u_in_04_value_range.py` (3 tests)
- [x] GREEN: cell ∉ `{0}∪[1,16]` → `ERR_VALUE_RANGE`
- [x] pytest: **3 passed**
- [x] 커밋: `feat(boundary): AC-FR01-04 ERR_VALUE_RANGE Green (A-04)`

#### A-05 · UT-06/07 empty count (AC-FR01-05) ✅
- [x] RED: `test_ut06_empty_count.py` (3 tests)
- [x] GREEN: `count(0) != 2` → `ERR_EMPTY_COUNT`
- [x] pytest: **3 passed**
- [x] 커밋: `feat(boundary): AC-FR01-05 ERR_EMPTY_COUNT Green (A-05)`

#### A-06 · UT-08 duplicate (AC-FR01-06) ✅
- [x] RED: `test_u_in_05_duplicate.py` (2 tests)
- [x] GREEN: non-zero 중복 → `ERR_DUPLICATE`
- [x] pytest: **2 passed**
- [x] 커밋: `feat(boundary): AC-FR01-06 ERR_DUPLICATE Green (A-06)`

#### A-07 · U-FLOW execute isolation (FR-01)
- [ ] RED: `test_u_flow_02_execute_isolation.py` — E004/E005만 *(null 격리는 A-01 포함)*
- [ ] GREEN: `ui_boundary` + invalid 입력 시 `execute` 0회
- [ ] pytest: `python -m pytest tests/boundary/test_u_flow_02_execute_isolation.py -v`
- [ ] 커밋 예: `feat(boundary): U-FLOW invalid execute 0-call Green (A-07)`

#### A-08 · UT-09 valid solve + U-OUT (AC-FR01-07 / FR-05)
- [ ] RED: `test_u_out_output_contract.py` Full RED + UT-09 *(미작성)*
- [ ] GREEN: valid grid → OK envelope, `int[6]` passthrough (Domain Mock 1회)
- [ ] pytest: `python -m pytest tests/boundary/test_u_out_output_contract.py -v`
- [ ] 커밋 예: `feat(boundary): UT-09 OK envelope Green (A-08)`

### Track B — Domain (A-01 이후 병렬)

#### B-01 · D-VAL magic validator (FR-04 / DT-01~08)
- [ ] RED: `test_d_val.py` Full RED (6 tests)
- [ ] GREEN: `is_magic_square()` — G0 true / broken sum·diag·set false
- [ ] pytest: `python -m pytest tests/entity/test_d_val.py -v`
- [ ] 커밋 예: `feat(entity): D-VAL is_magic_square Green (B-01)`

#### B-02 · D-LOC + D-MIS (FR-02/03 / DT-03~04)
- [ ] RED: `test_d_loc_01.py`, `test_d_mis_01.py` Full RED
- [ ] GREEN: `find_blank_coords()`, `find_not_exist_nums()`
- [ ] pytest: `python -m pytest tests/entity/test_d_loc_01.py tests/entity/test_d_mis_01.py -v`
- [ ] 커밋 예: `feat(entity): D-LOC/MIS blank + missing Green (B-02)`

#### B-03 · D-SOL two-cell solver (FR-05 / DT-05~07, DT-10)
- [ ] RED: `test_d_sol.py` Full RED (4 tests)
- [ ] GREEN: `solution()` — forward / reverse / unsolvable
- [ ] pytest: `python -m pytest tests/entity/test_d_sol.py -v`
- [ ] 커밋 예: `feat(entity): D-SOL solution Green (B-03)`

### Integration (A-08 + B-03 이후)

#### I-01 · IT-FAIL invalid E2E
- [ ] RED: `tests/integration/test_it_fail_*.py` *(미작성)* — IT-FAIL-01~02, 04
- [ ] GREEN: 실 Boundary + Control, Domain Mock **금지**, invalid → ERROR
- [ ] pytest: `python -m pytest tests/integration/ -v -k fail`
- [ ] 커밋 예: `feat(integration): IT-FAIL invalid E2E Green (I-01)`

#### I-02 · IT-OK solve E2E
- [ ] RED: `tests/integration/test_it_ok_*.py` *(미작성)* — IT-OK-01~03
- [ ] GREEN: E2E solve + save/load round-trip
- [ ] pytest: `python -m pytest tests/integration/ -v -k ok`
- [ ] 커밋 예: `feat(integration): IT-OK solve E2E Green (I-02)`

### Green 마일스톤 · 회귀

- [ ] **FR-01 입력 검증 Green** — A-01~A-06 완료
- [ ] **Domain Core Green** — B-01~B-03 완료
- [ ] **성공 경로 Green** — A-08 완료
- [ ] **Integration Green** — I-01~I-02 완료
- [ ] Boundary 레이어 커버리지 **85%+**
- [ ] Domain Logic 커버리지 **95%+**
- [ ] 전체 pytest 회귀 통과: `python -m pytest -v`

### Green 진행 흐름

```
Track A (순차)          Track B (병렬)
A-01 NULL ✅            B-01 D-VAL
A-02 ROWS               B-02 LOC/MIS
A-03 COLS               B-03 SOL
A-04 RANGE                    │
A-05 EMPTY                    │
A-06 DUPLICATE                │
A-07 FLOW ────────────────────┤
A-08 SUCCESS ◄────────────────┘
         │
         ▼
      I-01 IT-FAIL → I-02 IT-OK
```

---

## 미해결 항목

- **1차 사용자** — Mom Test 미완 (PRD Persona: TDD 학습자로 가정)
- **ECB harmonization** — PRD §22 DEC-01 (Judge/Solver → entity vs control)
- **PRD 검토 보완** — AC-ID 전수 Traceability, DT-07/12 AC (Report/07 P0~P1)
- **`pytest-cov` CI** — 커버리지 gate 미구성
- **DEF-001** — `magicsquare.boundary` **부분 해소** (A-01). U-OUT/U-FLOW는 `ui_boundary` 미구현으로 collection ERROR 잔존
- **RED 테스트 계약 drift** — `INVALID_SIZE` vs PRD `ERR_NULL_GRID` (DEF-002) · `resolve` vs `solve_partial_grid` (DEF-003)

---

## 로컬 실행

### 가상환경 (권장)

```powershell
cd c:\DEV\MagicSquare_
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

### 테스트

```powershell
# A-01 Green (5 passed)
python -m pytest tests/boundary/test_ac_fr01_01_null_grid.py -v

# User Entity (9 passed)
python -m pytest tests/entity/test_user.py -v

# Boundary 전체 (5 passed + 3 failed + 2 errors)
python -m pytest tests/boundary/ -v --continue-on-collection-errors

# 전체 (entity user 9 passed + boundary 혼재 + d_* 수집 ERROR)
python -m pytest -v --continue-on-collection-errors
```

### 커버리지 HTML

> Report/10 이후 `tests/entity/`에는 RED Skeleton(`test_d_*.py`)이 포함되어 **기본 수집이 중단**됩니다. User Entity만 보려면 아래 **권장** 명령을 사용하세요 ([Report/11](Report/11-coverage-html-qa-report.md), DEF-004).

```powershell
# 권장 — User Entity만 (9 passed, htmlcov 생성)
python -m pytest tests/entity/test_user.py --cov=src --cov-report=html
start htmlcov\index.html

# 터미널 누락 라인 + HTML
python -m pytest tests/entity/test_user.py --cov=src --cov-report=term-missing --cov-report=html

# 대안 — RED Skeleton 수집 ERROR 무시 (9 passed + 4 errors, exit 1)
python -m pytest tests/entity/ --continue-on-collection-errors --cov=src --cov-report=html
start htmlcov\index.html
```

> DEF-001 부분 해소 후 boundary A-01은 수집 성공. `test_d_*` Skeleton은 여전히 `entity.services` import ERROR ([Report/11](Report/11-coverage-html-qa-report.md), DEF-004).

---

## 방법론 참고

- **The Mom Test** — 가설이 아닌 관찰
- **5 Whys** — 표면 요구에서 구조적 불편 도출
- **Dual-Track TDD** — Boundary(UT-*) ∥ Domain(DT-*), Red → Green → Refactor

---

## 라이선스

미정
