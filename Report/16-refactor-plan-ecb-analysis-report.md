# Magic Square 프로젝트 — REFACTOR 계획 · ECB 분석 보고서

**작성 목적:** GREEN 13/13 · Golden Master(60 passed) 이후 **REFACTOR phase 착수 전** 코드 스멜·ECB 역할·SRP·테스트 갭 분석 및 리팩토링 계획 확정  
**대상:** 주니어 개발자 + Cursor AI 협업 학습 프로젝트  
**범위:** `control/solve_partial_magic_square.py` · `boundary/ui_boundary.py` · `boundary/gui/main_window.py` · 연관 `input_validator` · `two_cell_solver` · `.cursorrules` ECB  
**선행 문서:** `Report/02-tdd-design-report.md`, `Report/14-green-completion-pyqt-gui-report.md`, `Report/15-golden-master-regression-report.md`, `.cursorrules`  
**작성일:** 2026-05-29

**Transcript:** `Prompting/16-refactor-plan-ecb-analysis-prompt.md`

---

## Executive Summary

Green 13/13 · Golden Master **60 passed** 상태에서 REFACTOR phase 전제(전체 Green · observable behavior 불변 · E001~E007·int[6] 계약 유지) 하에 3개 핵심 파일을 분석했다.

| 항목 | 결과 |
|------|------|
| **TDD phase** | GREEN 완료 → **REFACTOR 계획 수립** (구현 미착수) |
| **pytest** | **60 passed** (boundary 27 · entity 21 · integration 12 incl. GM) |
| **ECB 1순위(P0)** | Control→Boundary envelope 역의존 · facade 이중화 · E001 drift · GUI 테스트 0% |
| **Entity 분리** | `two_cell_solver.solution()` — **위치 적합, Refactor 범위 제외** |
| **코드 수정** | **미수행** — 본 보고서는 계획·분석만 |

---

## STEP 1 — ECB 매핑 · 역할 현황

| 파일 (실경로) | ECB 역할 | 적합 여부 | 근거 (1줄) |
|---------------|----------|-----------|------------|
| `control/solve_partial_magic_square.py` | Control | **부분** | `solution()` 위임은 Control이나 envelope·E007 조립이 Boundary 책임을 Control에 침범 |
| `boundary/ui_boundary.py` | Boundary | **부분** | E001~E005 검증·Domain 0-call 준수; E006/E007 envelope 소유·facade SSOT 미완 |
| `boundary/gui/main_window.py` | Screen (Boundary 하위) | **부분** | `UIBoundary`만 호출; GUI 테스트 없음 · `except Exception` · fixture 중복 |

**추가 판단**

| 질문 | 답 |
|------|-----|
| `solve_partial_magic_square.py` → Entity vs Control? | **Control** — 알고리즘·int[6] 조립은 `entity/services/two_cell_solver.py` |
| `ui_boundary.py` Domain must_not? | **위반 없음** — 검증+위임; envelope 최종화는 Control에 위임 중 |
| `main_window.py` UI 외 책임? | **fixture·예외 폴백** — solvability·E00x 결정·합=34 계산 없음 |

---

## STEP 2 — 테스트 갭 (Step 1)

| 대상 | 1:1 `test_*.py` | 간접 커버 | Refactor 전 필요 |
|------|-----------------|-----------|------------------|
| `solve_partial_magic_square.py` | 없음 (`tests/control/` 없음) | IT-OK/IT-FAIL, GM-TC, `entry.resolve` | `tests/control/test_solve_partial_execute.py` **신규** |
| `ui_boundary.py` | 없음 | U-FLOW-02, IT-*, GM | `tests/boundary/test_ui_boundary.py` **신규** (U-OUT/UT-09/U-FLOW) |
| `main_window.py` | 없음 | — | `tests/boundary/gui/test_main_window.py` **신규** (offscreen PyQt) |

**현재 RED skeleton:** `pytest.fail` **0건** (Report/10 21건 → Green 전환 완료).

**테스트 없이 Refactor 금지 (1줄):** Refactor phase는 pytest PASS 유지가 전제이므로, GUI·Control envelope 분리는 회귀 안전망 없이 구조 변경 불가.

---

## STEP 3 — High 스멜 · SRP 위반 요약

### 3.1 High (계약·ECB)

| 파일:줄 | 스멜 | 우선순위 |
|---------|------|----------|
| `solve_partial_magic_square.py:5-37` | Control→Boundary import · envelope 조립 | P0 |
| `ui_boundary.py:20-35` + `entry.py:22-36` | validate→execute 이중 facade (DEF-003) | P0 |
| `input_validator.py:36-41` | null → `INVALID_SIZE` vs Report/02 `ERR_NULL_GRID` (DEF-002) | P0 |
| `main_window.py:118-121` | `except Exception` → E001~E007 envelope 우회 | P0 |
| `main_window.py:135-145` | int[6] unpack 실패 → unexpected 흡수 | P0 |

### 3.2 SRP — 함수 다중 역할

| 파일:줄 | 역할 1 | 역할 2 |
|---------|--------|--------|
| `solve_partial_magic_square.py:18-37` | Domain 오케스트레이션 | Boundary envelope 조립 |
| `ui_boundary.py:20-35` | E001~E005 검증 | Control 위임 |
| `main_window.py:39-47` | UI 구성 | fixture 데이터 주입 |
| `main_window.py:95-101` | 격자 데이터 주입 | UI 상태 갱신 |
| `main_window.py:111-126` | 입력·Boundary 호출 | 예외 폴백·응답 라우팅 |

### 3.3 UI 비즈니스 판단

**해당 없음** — 합=34 계산·Step A/B·E00x 코드 결정 없음; DTO→표시만.

### 3.4 Control vs Entity 혼재

| 구분 | 판단 |
|------|------|
| `solve_partial_magic_square.py` 내 Entity 알고리즘 | **없음** |
| `two_cell_solver.py`와 중복 | **없음** — Entity가 UC-D01~D05 전담 |
| 분리 필요 | **Boundary envelope** (Control에서 이동) |

---

## STEP 4 — 리팩토링 대상 목록 (우선순위 순)

| 순번 | 대상 파일 | 문제 | 적용 기법 | 우선순위 |
|:---:|---|---|---|:---:|
| 1 | `control/solve_partial_magic_square.py` | Control이 Boundary envelope·E007 조립 (`control→boundary` 금지 위반) | Extract Class / Move Method → `boundary/response_mapper.py` | **P0** |
| 2 | `boundary/ui_boundary.py` + `boundary/entry.py` | validate→Control 이중 facade (DEF-003) | Facade 통합 · spy/mock 대상 단일화 | **P0** |
| 3 | `boundary/input_validator.py` + `schemas.py` | E001 null code drift (DEF-002) | SSOT 정렬 (Red→Green 선행) | **P0** |
| 4 | `boundary/gui/main_window.py` | GUI 테스트 0% · Refactor gate 미충족 | Test-First (offscreen PyQt) | **P0** |
| 5 | `boundary/gui/main_window.py:118-121` | broad `except Exception` | Guard · envelope 분기만 | **P0** |
| 6 | `boundary/gui/main_window.py:28-33` | `EXAMPLE_GRID` fixture 3중 복제 | Move Fixture → `tests/conftest.py` | **P1** |
| 7 | `boundary/gui/main_window.py:135-145` | int[6] unpack·표시 혼재 | Extract Class → `result_presenter` | **P1** |
| 8 | `boundary/gui/main_window.py` | ERROR/Ready UI reset 중복 | Extract Method | **P1** |
| 9 | `boundary/ui_boundary.py:31` | 매 호출 `InputValidator()` 생성 | DI / Factory | **P1** |
| 10 | `boundary/input_validator.py` | magic `4`/`16`/`2` | Entity `MagicConstant` SSOT | **P1** |
| 11 | `control/solve_partial_magic_square.py:12` | `solution` import명 모호 | Rename (Entity track) | **P2** |
| 12 | `boundary/gui/main_window.py:49-93` | `_build_ui` 45줄 | Extract Method | **P2** |

### ECB 분리 순서

| 단계 | 작업 | 선행 |
|:---:|---|---|
| P0-1 | Control envelope → Boundary mapper | IT/GM PASS |
| P0-2 | facade 통합 + E001 정합 | UT-01 Red→Green |
| P0-3 | GUI 테스트 Green | offscreen |
| P1 | fixture · presenter · DRY · 상수 SSOT | P0 완료 |

---

## STEP 5 — 테스트 선행 필요 항목

### P0 — Refactor 착수 전 필수

| 함수 / 클래스 | 테스트 파일 | 검증 계약 |
|---------------|-------------|-----------|
| `SolvePartialMagicSquare.execute` | `tests/control/test_solve_partial_execute.py` | valid → result; unsolvable → mapper E007 |
| `UIBoundary.solve` | `tests/boundary/test_ui_boundary.py` | U-OUT, U-FLOW, UT-09 직접 |
| `validate_and_solve` / `resolve` | facade 통합 후 기존 UT 보강 | spy 대상 단일화 |
| `InputValidator.validate` (null) | `test_ac_fr01_01_null_grid.py` 보강 | E001 Report/02 정합 |
| `MainWindow._on_solve` 등 | `tests/boundary/gui/test_main_window.py` | OK/ERROR 표시 · Boundary mock |

### P1 — P0 Green 이후

| 대상 | 테스트 |
|------|--------|
| `boundary/response_mapper.py` (예정) | `tests/boundary/test_response_mapper.py` |
| Golden Master | `test_golden_master_magic_square.py` 유지 |

### Refactor 범위 제외

| 대상 | 근거 |
|------|------|
| `entity/services/two_cell_solver.solution` | `test_d_sol` + IT/GM Green |

---

## STEP 6 — 리팩토링 후 검증 방법

### 회귀 테스트

```powershell
python -m pytest tests/ -q
python -m pytest tests/boundary/ tests/entity/ tests/integration/ -q
python -m pytest tests/integration/test_golden_master_magic_square.py -v -m golden_master
python -m pytest tests/ --cov=magicsquare --cov-report=term-missing -q
```

**PASS 기준:** 0 failed · GM diff 없음 · `control/` → `boundary/` import **0건**.

### 외부 동작 불변 확인

| 항목 | 방법 | 기대 |
|------|------|------|
| E001~E007 | UT-01~08, IT-FAIL | code·message Report/02 완전 일치 |
| invalid → Domain 0-call | U-FLOW-02 | execute 0회 |
| int[6] passthrough | UT-09, U-OUT, IT-OK, GM-TC | 6요소·1-index·재정렬 없음 |
| Golden Master | GM-TC-01~05 | baseline diff 없음 |
| GUI smoke | `QT_QPA_PLATFORM=offscreen python -m magicsquare` | Solve OK/ERROR envelope 표시 |

### Refactor phase 완료 정의

- [ ] pytest 전체 PASS (기존 60 + 신규)
- [ ] Golden Master PASS
- [ ] E001~E007·int[6] assert 불변 (E001 정합 시 UT-01 Red→Green 선행)
- [ ] `rg "from magicsquare.boundary" src/magicsquare/control/` → 0건
- [ ] facade 단일 진입점
- [ ] GUI offscreen smoke PASS
- [ ] 커버리지: boundary ≥85%, entity ≥95%, 전체 ≥80%

---

## STEP 7 — 결함·후속

| ID | 상태 | Refactor 연계 |
|----|------|---------------|
| **DEF-002** | Open | P0 — E001 `ERR_NULL_GRID` SSOT |
| **DEF-003** | Open | P0 — facade·spy 통합 |
| **DEF-001** | 해소 | — |
| **커버리지 gate** | Open | Refactor 후 pytest-cov CI |
| **REFACTOR 구현** | **계획만** | P0 테스트 Green → 순차 Refactor |

---

## 한 줄 결론

**E001~E007·int[6] 계약을 유지한 채 1순위(P0)는 Control envelope을 Boundary로 이동하고 facade/E001을 통합한 뒤 GUI 테스트 게이트를 확보하는 것**이며, Entity(`two_cell_solver`)는 ECB상 적합하여 Refactor 범위에서 제외한다.
