# Magic Square 프로젝트 — Dual-Track RED 설계 보고서

**작성 목적:** FR-01~FR-05 전체 범위에 대한 **RED 단계 테스트 설계표**를 Dual-Track(UI Boundary / Domain Logic)으로 고정 (구현·테스트 코드·파일 저장 없음)  
**대상:** 주니어 개발자 + Cursor AI 협업 학습 프로젝트  
**범위:** Track A U-IN-* / U-OUT-* / U-FLOW-* · Track B D-LOC-* / D-MIS-* / D-VAL-* / D-SOL-* · G0~G3 · RED 검수 체크리스트  
**선행 문서:** `docs/PRD_MagicSquare.md`, `Report/02-tdd-design-report.md`, `.cursorrules`, `docs/test_plan.md`, `Report/08-test-plan-red-phase-report.md`  
**작성일:** 2026-05-29

---

## Executive Summary

본 단계에서 **TDD phase: RED** 규칙(구현·스켈레톤·pytest·파일 저장 금지) 하에, FR-01~FR-05 Dual-Track **RED 설계표**를 확정했다. Track A는 Boundary Failure envelope(E003~E005)와 `SolvePartialMagicSquare.execute` **0회** 격리를, Track B는 Domain 별칭 API(`find_blank_coords`, `find_not_exist_nums`, `is_magic_square`, `solution`)와 Logic Invariant I1~I11을 **Domain Mock 없이** 검증하도록 설계했다.

| 항목 | 결과 |
|------|------|
| **Track A 설계 건수** | 14건 (U-IN 11 + U-OUT 2 + U-FLOW 1) |
| **Track B 설계 건수** | 12건 (D-LOC 1 + D-MIS 1 + D-VAL 6 + D-SOL 4) |
| **격자 부록** | G0=FIX-MAGIC, G1=v0.2 placeholder, G2=DT-06, G3=DT-10 |
| **코드 산출** | 없음 (설계표만) |
| **기존 RED 코드** | `tests/boundary/test_ac_fr01_01_null_grid.py` (UT-01 부분, DEF-002 drift) |

**Transcript:** `Prompting/09-dual-track-red-design-prompt.md`

---

## STEP 1 — SSOT 및 계약 정합

### 1.1 참조 문서

| SSOT | 경로 | 본 설계에서 사용 |
|------|------|------------------|
| PRD | `docs/PRD_MagicSquare.md` v1.0 | FR-01~05, AC-FR01-* |
| TDD 설계 | `Report/02-tdd-design-report.md` | FIX-MAGIC, DT-03/06/10, ERR_* |
| Cursor Rules | `.cursorrules` | Dual-Track, UT-/DT-*, ECB |
| 테스트 플랜 | `docs/test_plan.md` | AC-FR01-01 앵커, cov 목표 |

### 1.2 v0.2 프롬프트 계약 vs Report/02

| v0.2 (설계표 ID) | Report/02 (구현 SSOT) | 비고 |
|------------------|----------------------|------|
| E003 null | ERR_NULL_GRID | AC-FR01-01 |
| E001 size | ERR_GRID_ROWS / ERR_GRID_COLS | v0.2는 size 통합; PRD는 행/열 분리 |
| E002 empty count | ERR_EMPTY_COUNT | |
| E004 range | ERR_VALUE_RANGE | |
| E005 duplicate | ERR_DUPLICATE | |
| `execute` 0회 | solve_partial_grid / Domain 0-call | U-FLOW-02 |
| G1 (2,2)(3,3) | DT-03 (3,3)(4,4) | **격자 불일치 — 부록 확정 필요** |

### 1.3 Short-circuit 순서

**본 RED 설계 (프롬프트):** `null → size → empty count → value range → duplicate`  
**Report/02 / PRD:** `NULL → ROWS → COLS → RANGE → EMPTY_COUNT → DUPLICATE`  

→ Green 구현 전 **한 가지 SSOT로 통일** 필요 (DEF-002 연계).

---

## STEP 2 — Track A: Boundary / UI Contract RED

### 2.1 입력 검증 (U-IN-*) — Domain 0회

| Test ID | Given 요약 | Then (code) | AC |
|---------|------------|-------------|-----|
| U-IN-01 | `matrix=null` | E003 | AC-FR01-01 |
| U-IN-02a | `matrix=[]` | E001 | AC-FR01-02 |
| U-IN-02b | 3×4 | E001 | AC-FR01-02 |
| U-IN-02c | 4×3 | E001 | AC-FR01-03 |
| U-IN-02d | 5×5 | E001 | AC-FR01-02 |
| U-IN-02e | `[[]]*4` | E001 | AC-FR01-03 |
| U-IN-03a | `0` 개수=0 | E002 | AC-FR01-05 |
| U-IN-03b | `0` 개수=3 | E002 | AC-FR01-05 |
| U-IN-04a | cell=17 | E004 | AC-FR01-04 |
| U-IN-04b | cell=-1 | E004 | AC-FR01-04 |
| U-IN-05 | non-zero 중복 5 | E005 | AC-FR01-06 |

**When (공통):** `InputValidator.validate(matrix)` — 코드 작성 전 호출 대상만 고정.

**Expected RED Failure:** `ModuleNotFoundError`, `AttributeError`, 또는 assertion fail (Failure envelope 미구현).

### 2.2 출력 계약 (U-OUT-*)

| Test ID | Given | When | Then |
|---------|-------|------|------|
| U-OUT-01 | G1 | `UIBoundary.solve(matrix)` | `len(result)==6`, status OK |
| U-OUT-02 | G1 | 동일 | r,c ∈ [1,4] 1-index |

**전제:** 유효 입력; Track A에서 `execute` mock 반환 `[2,2,7,3,3,10]` 허용.

### 2.3 흐름 격리 (U-FLOW-02)

| Test ID | Given | When | Then |
|---------|-------|------|------|
| U-FLOW-02 | invalid (null 대표) | `UIBoundary.solve` + execute spy | `call_count==0` |

---

## STEP 3 — Track B: Domain / Logic RED

### 3.1 설계용 API 별칭 (구현명 미확정)

| 별칭 | 후보 책임 | Invariant |
|------|-----------|-----------|
| `find_blank_coords()` | EmptyCellLocator | I6 (INV-D2) |
| `find_not_exist_nums()` | MissingNumberFinder | I7, I11 (INV-D1) |
| `is_magic_square()` | MagicSquareValidator | I1~I5 (INV-D3) |
| `solution()` | TwoCellSolver / Use Case | I8~I10 (INV-D6, D7) |

**Domain Mock 금지** — Track B 전건.

### 3.2 Logic RED 카탈로그

| Test ID | Given | Then | FR / AC |
|---------|-------|------|---------|
| D-LOC-01 | G1 | (2,2), (3,3) row-major | FR-02 |
| D-MIS-01 | G1 | {7, 10} 오름차순 | FR-03 |
| D-VAL-01 | G0 | true | FR-04 |
| D-VAL-02 | G0 행 합 깨짐 | false | FR-04 |
| D-VAL-03 | G0 열 합 깨짐 | false | FR-04 |
| D-VAL-04 | G0 대각 깨짐 | false | FR-04 |
| D-VAL-05 | 1~16 위반 | false | FR-04 |
| D-VAL-06 | 완전 격자에 0 포함 | false | FR-04 |
| D-SOL-01 | G1 | `[2,2,7,3,3,10]` | FR-05 |
| D-SOL-02 | G2 (DT-06) | `[1,1,16,4,4,1]` | FR-05 |
| D-SOL-03 | G3 (DT-10) | UnsolvableDomainError | FR-05 |
| D-SOL-04 | G1 | len=6, coords 1-index | FR-05 |

**Expected RED Failure:** `ImportError`, `AttributeError`, `AssertionError` (미구현).

---

## STEP 4 — 격자 부록 G0~G3

| ID | 정의 | Report/02 |
|----|------|-----------|
| **G0** | 완성 마방진 | FIX-MAGIC |
| **G1** | 빈칸 (2,2),(3,3); 누락 {7,10}; 기대 `[2,2,7,3,3,10]` | v0.2 전용 placeholder |
| **G2** | Step A 실패·B 성공 | DT-06 입력 |
| **G3** | Step A·B 실패 | DT-10 / NO_COMPLETION |

**G0 리터럴:**

```
[16,  3,  2, 13]
[ 5, 10, 11,  8]
[ 9,  6,  7, 12]
[ 4, 15, 14,  1]
```

---

## STEP 5 — RED 설계 검수

| # | 항목 | 결과 |
|---|------|------|
| 1 | Boundary E00x Failure schema (예외 아님) | Pass |
| 2 | invalid → execute 0회 | Pass |
| 3 | U-IN vs U-OUT 분리 | Pass |
| 4 | Logic Track Domain Mock 없음 | Pass |
| 5 | I1~I11 · AC-FR* 추적 | Pass |
| 6 | 코드/스켈레톤/파일 미작성 | Pass |

---

## STEP 6 — 권장 RED 착수 순서

| 순서 | Track A | Track B |
|------|---------|---------|
| 1 | U-IN-01, U-FLOW-02 | D-VAL-01 |
| 2 | U-IN-02a~e | D-VAL-02~04 |
| 3 | U-IN-03a,b, 04a,b, 05 | D-LOC-01, D-MIS-01 |
| 4 | U-OUT-01, 02 | D-SOL-01~04 |

**한 사이클 = Test ID 1개 → pytest FAIL → Green 최소 구현 → Refactor.**

---

## 교차 이슈

| ID | 이슈 | 권장 |
|----|------|------|
| X-01 | E00x vs ERR_* 이중 체계 | Green 전 ErrorFactory SSOT 단일화 |
| X-02 | G1 vs DT-03 격자 불일치 | v0.2 부록 또는 Report/02 중 선택 |
| X-03 | 기존 boundary RED `INVALID_SIZE` | DEF-002 — 설계표는 E003/ERR_NULL_GRID |
| X-04 | `resolve()` vs `execute` | DEF-003 — `SolvePartialMagicSquare.execute` |

---

## Traceability (FR → RED Test ID)

| FR | Track A | Track B |
|----|---------|---------|
| FR-01 | U-IN-01~05, U-FLOW-02 | — |
| FR-02 | U-OUT-02 | D-LOC-01 |
| FR-03 | — | D-MIS-01 |
| FR-04 | — | D-VAL-01~06 |
| FR-05 | U-OUT-01, U-OUT-02 | D-SOL-01~04 |

---

## 다음 단계

- [ ] SSOT 통일: E00x ↔ ERR_* · short-circuit 순서 · G1 리터럴
- [ ] U-IN-01 pytest RED 코드 작성 (1 TC-ID = 1 Red)
- [ ] D-VAL-01 pytest RED 코드 작성 (DT-01 병행)
- [ ] `defect_list.md` DEF-002·003 해소 후 설계표와 코드 정합

---

## 변경 이력

| 날짜 | 내용 |
|------|------|
| 2026-05-29 | FR-01~05 Dual-Track RED 설계표 확정 → Report/09 · Prompting/09 Export |

---

## 부록 A — 생성·갱신 파일

| 경로 | 설명 |
|------|------|
| `Report/09-dual-track-red-design-report.md` | 본 보고서 |
| `Prompting/09-dual-track-red-design-prompt.md` | Transcript Export |

## 부록 B — 전체 설계표

전체 Given/When/Then·Expected RED Failure 열은 대화 산출 **RED 설계표 본문** 및 본 Report STEP 2~3 요약표를 참조한다. (코드 파일로는 미저장 — 설계 단계 산출물)
