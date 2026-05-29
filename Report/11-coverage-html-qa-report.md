# Magic Square 프로젝트 — 커버리지 HTML QA 보고서

**작성 목적:** Report/10 RED Skeleton 추가 이후 **pytest-cov HTML 리포트** 생성 실패 원인 분석 및 workaround 확정  
**대상:** 주니어 개발자 + Cursor AI 협업 학습 프로젝트  
**범위:** `htmlcov/` 생성 명령 · 수집 ERROR(DEF-001·004) · entity `test_d_*` RED 영향 · 검증된 실행 매트릭스  
**선행 문서:** `Report/08-test-plan-red-phase-report.md`, `Report/10-dual-track-red-skeleton-report.md`, `defect_list.md`, `README.md`  
**작성일:** 2026-05-29

---

## Executive Summary

로컬에서 `python -m pytest tests/entity/ --cov=src --cov-report=html` 실행 시 **4 errors during collection**으로 세션이 중단되어 `htmlcov/`가 생성되지 않는 문제가 보고되었다. 원인은 Report/10에서 추가한 Track B RED Skeleton(`test_d_*.py`) 4파일이 **미구현** `magicsquare.entity.services`를 module-level import하기 때문이다. **workaround**로 `test_user.py` 단독 지정 또는 `--continue-on-collection-errors` 사용 시 HTML 생성이 확인되었다.

| 항목 | 결과 |
|------|------|
| **증상** | `ModuleNotFoundError: magicsquare.entity.services` → 수집 중단 |
| **영향 명령** | `tests/entity/`, `--ignore=tests/boundary` (entity 전체 수집 시) |
| **검증된 workaround** | `tests/entity/test_user.py` 단독 → **9 passed**, `htmlcov/` 생성 |
| **대안** | `tests/entity/ --continue-on-collection-errors` → 9 passed + 4 errors, HTML 생성 |
| **근본 해결** | DEF-001·005 Green — `boundary/`, `entity/services/` 구현 |
| **DEF-004 상태** | Open — workaround 문서화 완료 |

**Transcript:** `Prompting/11-coverage-html-qa-prompt.md`

---

## STEP 1 — 증상 재현

### 1.1 실패 명령 (사용자 실행)

```powershell
python -m pytest tests/entity/ --cov=src --cov-report=html
python -m pytest --ignore=tests/boundary --cov=src --cov-report=html
```

### 1.2 에러 메시지

```
ModuleNotFoundError: No module named 'magicsquare.entity.services'
!!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
```

| ERROR 파일 | import 대상 |
|------------|-------------|
| `tests/entity/test_d_loc_01.py` | `empty_cell_locator.find_blank_coords` |
| `tests/entity/test_d_mis_01.py` | `missing_number_finder.find_not_exist_nums` |
| `tests/entity/test_d_val.py` | `magic_square_validator.is_magic_square` |
| `tests/entity/test_d_sol.py` | `two_cell_solver.solution` |

---

## STEP 2 — 원인 분석

### 2.1 DEF-004 vs Report/10 이후 변화

| 시점 | `tests/entity/` 수집 | HTML 생성 |
|------|------------------------|-----------|
| Report/08 (User만) | 9 items, 9 passed | ✅ 가능 |
| Report/10 (+ test_d_* 4파일) | 9 items + **4 errors** | ❌ 기본 명령 실패 |

Report/08·README에 기록된 `pytest tests/entity/` workaround는 **Report/10 이전**에는 유효했으나, Track B Skeleton 추가 후 **갱신 필요**.

### 2.2 RED 설계와의 정합

| 관점 | 설명 |
|------|------|
| **의도된 RED** | Skeleton top-level import → collection ERROR = RED (Report/10) |
| **QA 목적** | User Entity Green 커버리지만 HTML로 확인 가능해야 함 |
| **충돌 해소** | 테스트 **경로를 좁히거나** `--continue-on-collection-errors` 사용 |

---

## STEP 3 — 검증된 workaround

### 3.1 권장 — User 테스트 단독 (exit code 0)

```powershell
python -m pytest tests/entity/test_user.py --cov=src --cov-report=html
start htmlcov\index.html
```

**결과 (2026-05-29):** 9 passed · `Coverage HTML written to dir htmlcov`

### 3.2 대안 — entity 전체 + 수집 ERROR 무시 (exit code 1)

```powershell
python -m pytest tests/entity/ --continue-on-collection-errors --cov=src --cov-report=html
start htmlcov\index.html
```

**결과:** 9 passed, 4 errors · HTML 생성됨 (errors는 RED Skeleton)

### 3.3 boundary 제외 + User 단독

```powershell
python -m pytest tests/entity/test_user.py --ignore=tests/boundary --cov=src --cov-report=html
start htmlcov\index.html
```

`--ignore=tests/boundary`만으로는 `test_d_*` collection ERROR가 해소되지 않음.

### 3.4 현재 실패하는 명령 (참고)

| 명령 | 이유 |
|------|------|
| `pytest tests/entity/ --cov=...` | test_d_* 4 errors → 중단 |
| `pytest --ignore=tests/boundary --cov=...` | 동일 (entity test_d_* 포함) |
| `pytest --cov=src --cov-report=html` (전체) | boundary + entity test_d_* errors |

---

## STEP 4 — 실행 매트릭스 (갱신)

| 목적 | 명령 | 기대 |
|------|------|------|
| User 커버리지 HTML | `pytest tests/entity/test_user.py --cov=src --cov-report=html` | 9 passed, htmlcov ✅ |
| 터미널 + HTML | 위 + `--cov-report=term-missing` | 누락 라인 표시 |
| RED Skeleton 포함 | `--continue-on-collection-errors` | 9 passed + errors, htmlcov ✅ |
| 전체 gate (Green 후) | `pytest --cov=src --cov-fail-under=80` | DEF-001 해결 후 |

---

## STEP 5 — 결함·문서 연계

| ID | 연관 | 조치 |
|----|------|------|
| DEF-001 | `magicsquare.boundary` 없음 | Green: boundary 최소 구현 |
| DEF-004 | 전체 pytest → htmlcov 미생성 | README workaround 갱신 (본 Report) |
| DEF-005 | ECB 레이어 미착수 | entity/services Green 시 test_d_* 수집 성공 |
| DEF-006 | Domain Track 미구현 | D-* Skeleton → Full RED → Green 순 |

---

## STEP 6 — README 갱신 항목

`README.md` **커버리지 HTML** 섹션:

- ~~`pytest tests/entity/`~~ → `pytest tests/entity/test_user.py` (권장)
- `--continue-on-collection-errors` 대안 추가
- Report/10 이후 entity 폴더 전체 수집 시 4 errors 명시

---

## 다음 단계

- [ ] DEF-004 workaround README 반영 확인
- [ ] Green 후 `tests/entity/` 전체 커버리지 명령 회귀 검증
- [ ] CI: RED 단계에서는 `test_user.py`만 cov gate (선택)
- [ ] `entity/services/` Green — D-VAL-01 1 cycle

---

## 변경 이력

| 날짜 | 내용 |
|------|------|
| 2026-05-29 | 커버리지 HTML 실패 분석 · workaround 검증 → Report/11 · Prompting/11 Export |

---

## 부록 A — 생성·갱신 파일

| 경로 | 설명 |
|------|------|
| `Report/11-coverage-html-qa-report.md` | 본 보고서 |
| `Prompting/11-coverage-html-qa-prompt.md` | Transcript Export |
| `README.md` | 커버리지 HTML 명령 갱신 |

## 부록 B — 관련 문서

| 문서 | 경로 |
|------|------|
| RED Skeleton | `Report/10-dual-track-red-skeleton-report.md` |
| 테스트 플랜·RED QA | `Report/08-test-plan-red-phase-report.md` |
| 결함 목록 | `defect_list.md` |
