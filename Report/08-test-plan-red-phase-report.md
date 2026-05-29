# Magic Square 프로젝트 — 테스트 플랜·RED 단계·QA 보고서

**작성 목적:** AC-FR01-01 앵커 테스트 플랜 수립, Boundary RED 테스트 작성, 결함 목록화, 커버리지·venv 운영 이슈를 한 흐름으로 정리  
**대상:** 주니어 개발자 + Cursor AI 협업 학습 프로젝트  
**범위:** 샘플 AC 선정 → `docs/test_plan.md` → README RED 체크리스트 → `tests/boundary/` RED → `defect_list.md` (Green 구현 제외)  
**선행 문서:** `docs/PRD_MagicSquare.md`, `Report/02-tdd-design-report.md`, `Report/07-prd-creation-and-review-report.md`  
**작성일:** 2026-05-29

---

## Executive Summary

본 단계에서 FR-01 선행 조건 **AC-FR01-01**(`grid is null` → Boundary ERROR, Domain **0회**)을 앵커로 테스트 설계·RED 착수를 진행했다. 시니어 QA 관점 **테스트 계획서**(`docs/test_plan.md`)를 작성하고, pytest 기반 Boundary RED 테스트 5건·결함 목록 6건을 등록했다. **Green 구현(`src/magicsquare/boundary/`)은 미착수**이며, 전체 `pytest`는 boundary 수집 단계에서 실패하는 **의도된 RED** 상태다.

| 항목 | 결과 |
|------|------|
| **앵커 AC** | AC-FR01-01 (UT-01) — `grid=None` / PRD·Report/02: `ERR_NULL_GRID` |
| **테스트 플랜** | `docs/test_plan.md` (TP-MSQ-FR01-001) |
| **RED 테스트** | `tests/boundary/test_ac_fr01_01_null_grid.py` (5 methods) |
| **결함 목록** | `defect_list.md` (DEF-001~006, Open) |
| **README** | RED To-Do, defect 링크, 로컬 실행(venv·cov) 갱신 |
| **Boundary 구현** | ❌ 미착수 (`magicsquare.boundary` 없음) |
| **계약 drift** | RED 테스트가 `INVALID_SIZE` 기대 — PRD는 `ERR_NULL_GRID` (DEF-002) |

**pytest (2026-05-29 기준):**

| Suite | 결과 |
|-------|------|
| `tests/entity/` | **9 passed** |
| `tests/boundary/` | **1 error** (collection — `ModuleNotFoundError: magicsquare.boundary`) |
| `pytest` (전체) | 수집 중단 — boundary ERROR |

**커버리지:** `tests/entity/` + `--cov-report=html` → `htmlcov/` 생성 가능. 전체 `pytest --cov=src`는 boundary 수집 실패 시 `htmlcov` 미생성 (DEF-004).

**Transcript:** `Prompting/08-test-plan-red-phase-prompt.md`

---

## STEP 1 — 샘플 AC 선정 (AC-FR01-01)

### 1.1 선택 기준

| # | 기준 | 충족 |
|---|------|------|
| 1 | FR-01 검증 순서 최선행 (`NULL` 단락) | ✅ |
| 2 | Boundary 비즈니스 로직 직접 검증 | ✅ |
| 3 | Boundary·Domain 진입점 격리 동시 검증 | ✅ (UT-01 + mock 0회) |

### 1.2 확정 샘플

| 항목 | 값 |
|------|-----|
| **AC ID** | AC-FR01-01 |
| **FR** | FR-01 Input Verification (Boundary) |
| **입력** | `grid = None` |
| **PRD·Report/02 기대** | `code="ERR_NULL_GRID"`, `message="Input grid is null."` |
| **TC-ID** | UT-01 |
| **BR** | BR-15 (invalid input → Domain 0-call) |

초기 요청 예시의 `INVALID_SIZE` / `"Grid must be 4x4."`는 **크기 불일치(AC-FR01-02·03)** 계열로, AC-FR01-01 SSOT와 구분함.

---

## STEP 2 — 테스트 계획서 (`docs/test_plan.md`)

### 2.1 산출물

| Field | Value |
|-------|-------|
| Document ID | TP-MSQ-FR01-001 |
| Stack | Python **3.10+**, pytest, pydantic, unittest.mock |
| P0 | UT-01 (`grid=None`, `ERR_NULL_GRID`, Domain 0회) |
| P1 | UT-02·03 (rows/cols) — AC-FR01-01 범위 외 |
| 커버리지 목표 | Domain ≥95%, Boundary ≥85%, Total ≥80% |

### 2.2 pytest-cov 전략

```bash
pip install pytest-cov
python -m pytest --cov=src --cov-report=term-missing
python -m pytest tests/entity/ --cov=src --cov-report=html
```

---

## STEP 3 — README RED 단계 To-Do

### 3.1 반영 내용

- `docs/test_plan.md` 링크 및 **AC-FR01-01** 앵커 명시
- Track A P0: `ERR_NULL_GRID` / `Input grid is null.` (PRD SSOT)
- Track A P1: `[]`, 3×4 → `ERR_GRID_ROWS` (별도 RED)
- 결함 목록: `defect_list.md` 생성 체크 완료

### 3.2 미완료

- TC-A-01~07, TC-B-01~04 RED 체크박스 — Green 전까지 미체크
- 회귀 전체 통과 체크박스 — Open

---

## STEP 4 — Boundary RED 테스트

### 4.1 파일

| 경로 | 설명 |
|------|------|
| `tests/boundary/__init__.py` | Boundary 테스트 패키지 |
| `tests/boundary/test_ac_fr01_01_null_grid.py` | AC-FR01-01 RED 5건 |

### 4.2 테스트 유형 (5건)

| # | 유형 | 테스트 함수 (요약) |
|---|------|-------------------|
| 1 | 정상 실패 반환 | `test_none_grid_returns_error_with_invalid_size_code` |
| 2 | 메시지 동일성 | `test_none_grid_message_matches_prd_section_8_1_exactly` |
| 3 | 격리 (mock) | `test_none_grid_skips_resolve_zero_calls_isolation` |
| 4 | pydantic envelope | `test_none_grid_error_envelope_validates_with_pydantic` |
| 5 | null 경계 + scope | `test_none_grid_explicit_none_null_boundary_rejection` |

### 4.3 RED 상태 (의도)

```
ModuleNotFoundError: No module named 'magicsquare.boundary'
```

`from magicsquare.boundary.entry import validate_and_solve` — **구현 전 정상 RED**.

### 4.4 계약·아키텍처 drift (Green 전 해소 필요)

| 이슈 | RED 테스트 | SSOT (PRD / Report/02 / README) |
|------|------------|----------------------------------|
| Error code | `INVALID_SIZE` | `ERR_NULL_GRID` |
| Message | `Grid must be 4x4.` | `Input grid is null.` |
| Domain mock | `resolve()` | `solve_partial_grid` |

→ **DEF-002**, **DEF-003** 참고.

---

## STEP 5 — 결함 목록 (`defect_list.md`)

| ID | Severity | 요약 |
|----|----------|------|
| DEF-001 | Critical | `magicsquare.boundary` 미구현 → 수집 실패 |
| DEF-002 | High | Error code/message SSOT 불일치 |
| DEF-003 | High | `resolve()` vs `solve_partial_grid` mock 대상 불일치 |
| DEF-004 | Medium | 전체 pytest 시 `htmlcov` 미생성 |
| DEF-005 | Medium | Boundary/Control 레이어 미착수 |
| DEF-006 | Low | Domain Track (DT-01~) 미착수 |

**상태:** 6 Open / 0 Closed

---

## STEP 6 — 로컬 QA 운영 (venv·커버리지)

### 6.1 가상환경

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

### 6.2 실행 매트릭스

| 명령 | 기대 |
|------|------|
| `python -m pytest tests/entity/` | 9 passed |
| `python -m pytest tests/boundary/` | collection ERROR (RED) |
| `python -m pytest --ignore=tests/boundary --cov=src --cov-report=html` | htmlcov 생성 |
| `python -m pytest tests/entity/ --cov=src --cov-report=html` | entity 100%, htmlcov 생성 |

---

## Traceability (본 단계)

| Concept | FR | AC | TC | Artifact |
|---------|----|----|-----|----------|
| Null grid | FR-01 | AC-FR01-01 | UT-01 | test_plan, boundary test, defect_list |
| Domain 0-call | FR-01 | AC-FR01-01~06 | UT-01~08 | test_plan §7, DEF-001 |
| Test plan | FR-01 | AC-FR01-* | UT-01~08 | `docs/test_plan.md` |
| Defect mgmt | — | — | — | `defect_list.md` |

---

## 교차 이슈

| ID | 이슈 | 권장 조치 |
|----|------|-----------|
| X-01 | RED 테스트 vs PRD Error 표 | Green 전 테스트를 `ERR_NULL_GRID`로 정렬 (P0) |
| X-02 | PRD §8.1 vs §10·§13 | 테스트 docstring의 §8.1은 User Journey §8; Error SSOT는 §13.1 |
| X-03 | Report/07 권장 UT-04 Red vs 본 단계 UT-01 Red | 병행 가능 — UT-01(null)이 검증 순서상 선행 |
| X-04 | `pyproject.toml` dev에 pydantic 추가됨 | boundary envelope 테스트용 |

---

## 다음 단계 (권장)

- [ ] **DEF-002·003 해소:** boundary RED 테스트를 PRD SSOT·`solve_partial_grid` mock으로 정렬
- [ ] **DEF-001 Green:** `src/magicsquare/boundary/entry.py` — `validate_and_solve(None)` → `ERR_NULL_GRID`
- [ ] UT-01 5건 PASS 확인 후 README TC-A-01~04 체크
- [ ] UT-02·03 (P1) RED 병행
- [ ] DT-01 Red (Domain Track) — Report/07·PRD Dual-Track 교차 진행
- [ ] `pytest --cov=src --cov-fail-under=80` CI gate (boundary Green 후)

---

## 변경 이력

| 날짜 | 내용 |
|------|------|
| 2026-05-29 | test_plan · boundary RED · defect_list · README RED/실행 갱신 → Report/08·Prompting/08 Export |

---

## 부록 A — 생성·갱신 파일

| 경로 | 설명 |
|------|------|
| `docs/test_plan.md` | FR-01 / AC-FR01-01 테스트 계획서 |
| `tests/boundary/test_ac_fr01_01_null_grid.py` | UT-01 RED (5 tests) |
| `defect_list.md` | 결함 DEF-001~006 |
| `README.md` | RED To-Do, 문서 링크, 로컬 실행 |
| `pyproject.toml` | dev: `pydantic>=2.0` |
| `Report/08-test-plan-red-phase-report.md` | 본 보고서 |
| `Prompting/08-test-plan-red-phase-prompt.md` | Transcript Export |

## 부록 B — 관련 문서

| 문서 | 경로 |
|------|------|
| PRD | `docs/PRD_MagicSquare.md` |
| TDD 설계 (TC-ID SSOT) | `Report/02-tdd-design-report.md` |
| PRD 작성·검토 | `Report/07-prd-creation-and-review-report.md` |
| 결함 목록 | `defect_list.md` |
