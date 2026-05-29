# Magic Square — 결함 목록 (Defect List)

| Field | Value |
|---|---|
| **Document ID** | DEF-MSQ-001 |
| **Version** | 1.0 |
| **Status** | Open (RED 단계) |
| **Last Updated** | 2026-05-29 |
| **Related** | [test_plan.md](docs/test_plan.md), [PRD](docs/PRD_MagicSquare.md) §10 FR-01, [Report/02](Report/02-tdd-design-report.md) UT-01 |

---

## 요약

| Severity | Open | Closed |
|---|---|---|
| Critical | 1 | 0 |
| High | 2 | 0 |
| Medium | 2 | 0 |
| Low | 1 | 0 |
| **Total** | **6** | **0** |

---

## 결함 상세

| ID | Severity | AC ID | 재현 절차 | 기대값 | 실제값 | 근본 원인 | 수정 요약 |
|---|---|---|---|---|---|---|---|
| DEF-001 | Critical | AC-FR01-01 | 1. venv 활성화<br>2. `python -m pytest` 또는 `python -m pytest tests/boundary/` 실행 | Boundary 진입점 import 성공, UT-01 RED 테스트 수집·실행 | `ModuleNotFoundError: No module named 'magicsquare.boundary'` (수집 단계 중단) | `src/magicsquare/boundary/` 패키지·`entry.py`·`validate_and_solve` 미구현 | ECB Boundary 레이어 스켈레톤 추가: `boundary/entry.py`에 `validate_and_solve` 최소 시그니처 |
| DEF-002 | High | AC-FR01-01 | — | `ERR_NULL_GRID` / `Input grid is null.` | — | RED 테스트 SSOT drift | **Closed** — REFACTOR ①: 구현·UT-01 테스트 Report/02 정렬 |
| DEF-003 | High | AC-FR01-01 | — | `SolvePartialMagicSquare.execute` mock | — | `resolve` vs Control execute | **Closed** — REFACTOR ①: facade 통합 · execute patch 통일 |
| DEF-004 | Medium | AC-FR01-01 | 1. `python -m pytest --cov=src --cov-report=html` 실행 | 테스트 세션 완료 후 `htmlcov/` 생성 | 수집 ERROR로 세션 중단 → `htmlcov` 미생성 (boundary 포함 시) | DEF-001과 동일 — boundary 수집 실패 | DEF-001 해결 전 workaround: `pytest tests/entity/ --cov=src --cov-report=html` 또는 `--ignore=tests/boundary` |
| DEF-005 | Medium | FR-01 (전체) | 1. `src/magicsquare/` 디렉터리 구조 확인<br>2. FR-01 BoundaryValidator / ErrorFactory / ResponseMapper 존재 여부 확인 | Boundary 검증 순서 `NULL→ROWS→…` 구현체 존재 | `boundary/`, `control/` 패키지 없음 (entity만 존재) | 마방진 핵심 ECB 레이어 미착수 | FR-01 Green: `BoundaryValidator` + 고정 Error message + `ResponseMapper` 순차 구현 (UT-01→UT-08) |
| DEF-006 | Low | FR-02~05 | 1. `python -m pytest tests/entity/ --cov=src/magicsquare/entity` 실행<br>2. NFR-01 Domain Logic 95%+ gate 대조 | `entity` + `control` Domain 로직 line coverage ≥ 95% | User Entity만 100%; `MagicSquareJudge`·Solver 등 **미구현** (DT-01~ 미착수) | Domain Track RED 미시작 | Track B: DT-01 Red부터 병행; coverage gate는 control/entity domain 경로 합산 기준 적용 |

---

## 재현 명령 (공통)

```powershell
cd c:\DEV\MagicSquare_
.\.venv\Scripts\Activate.ps1
python -m pytest -v
python -m pytest tests/boundary/test_ac_fr01_01_null_grid.py -v
```

**Entity만 (통과·htmlcov 생성):**

```powershell
python -m pytest tests/entity/ --cov=src --cov-report=html
```

---

## AC-FR01-01 (UT-01) 종료 기준 — 결함 해소 체크

- [ ] DEF-001: `magicsquare.boundary` import 성공
- [ ] DEF-002: Error code/message가 PRD §13.1·Report/02와 일치
- [ ] DEF-003: Domain mock/spy 대상이 `solve_partial_grid`(또는 합의된 port)와 일치
- [ ] DEF-004: `python -m pytest --cov=src --cov-report=html` → `htmlcov/` 생성
- [ ] UT-01 5건 RED → Green → 전체 회귀 PASS

---

## 변경 이력

| Date | Author | Change |
|---|---|---|
| 2026-05-29 | QA Lead | 초기 등록 (RED 단계 수집·계약 drift·커버리지 차단) |
