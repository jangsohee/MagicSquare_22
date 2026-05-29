# Magic Square — 테스트 플랜·RED 단계·QA (transcript)
_Exported on 2026-05-29 from Cursor — AC-FR01-01 선정 → test_plan → README RED → boundary RED → defect_list → Report/08 Export_  
_선행: `docs/PRD_MagicSquare.md`, `Report/02-tdd-design-report.md`, `Report/07-prd-creation-and-review-report.md`_

---

**User**

`docs/PRD_MagicSquare.md` 참고하여 테스트 플랜 작성용 샘플 예제 1개 선택.

선택 기준:
1. FR-01 AC 중 가장 선행 — 입력 유효성 (NULL)
2. `grid is None` → 비즈니스 로직 검증
3. Boundary·Domain 격리 동시 검증

출력: AC ID, FR, 입력/기대, 선택 이유 2줄. **코드 작성 금지.**

---

**Cursor**

**선택 예제**

| 항목 | 값 |
|------|-----|
| AC ID | AC-FR01-01 |
| FR | FR-01, §10·§13.1 |
| 입력 | `grid = None` |
| PRD·Report/02 기대 | `ERR_NULL_GRID`, `Input grid is null.` |
| TC-ID | UT-01 |

초기 예시 `INVALID_SIZE` / `Grid must be 4x4.`는 AC-FR01-02·03(크기) 계열로 AC-FR01-01과 구분.

---

**User**

선택 샘플 기반 **시니어 QA 테스트 계획서** 작성.

포함: pytest 범위/우선순위, 경계값(`None`, `[]`, `[[]]*4`, 3×4·4×3·5×5 — 4×4 정상 제외), mock/spy, 커버리지 95%/85%, pytest-cov 명령.

**저장:** `docs/test_plan.md`

---

**Cursor**

`docs/test_plan.md` (TP-MSQ-FR01-001) 작성.

- P0: UT-01 / AC-FR01-01 — `ERR_NULL_GRID`, Domain 0회
- P1: UT-02·03 — size mismatch (AC-FR01-01 범위 외)
- Stack: Python 3.10+ (이후 사용자 요청으로 버전 문구 조정)
- pytest-cov: `--cov=src --cov-report=term-missing` / html / `--cov-fail-under`

---

**User**

README에 **RED 단계 To-Do** 체크리스트 삽입 (제공 형식). 기존 내용 유지.

---

**Cursor**

`## RED 단계 To-Do 리스트` — `## 진행 상황`과 `## 미해결 항목` 사이 삽입.

초기 삽입 시 `INVALID_SIZE` 문구 포함 → 이후 PRD SSOT로 README 정렬.

---

**User**

선택 예제가 AC-FR01-01에 맞는지 확인 요청.

---

**Cursor**

| 문서 | AC-FR01-01 정합 |
|------|-----------------|
| `test_plan.md` | ✅ `ERR_NULL_GRID` |
| README (수정 후) | ✅ |
| boundary RED 테스트 | ❌ `INVALID_SIZE` drift (DEF-002) |

---

**User**

`test_plan.md` Python **3.13+** → **3.10+** 로 변경.

README를 선택 예제(PRD SSOT)에 맞게 수정.

---

**Cursor**

- `test_plan.md`: `Python 3.10+`
- README: TC-A-02/03 → `ERR_NULL_GRID` / `Input grid is null.`; P0/P1 구분; `solve_partial_grid`

---

**User**

[P] QA. AC-FR01-01 범위 **아이템 타입별 최소 5개** pytest RED 테스트.

요청 계약 예: `INVALID_SIZE`, `Grid must be 4x4.`; `resolve()` mock; Given-When-Then; `# AC-FR-01-01`; `test_[입력]_[동작]_[포인트]`.

**RED — pytest 실패 상태.**

---

**Cursor**

- `tests/boundary/test_ac_fr01_01_null_grid.py` — 5 tests
- `pyproject.toml` dev: `pydantic>=2.0`
- 수집 실패: `ModuleNotFoundError: magicsquare.boundary` (의도된 RED)

AC-FR01-02~05 입력(`[]`, 3×4)은 별도 파일·스프린트로 제외.

---

**User**

가상환경에서 테스트·**HTML 커버리지** 방법.

---

**Cursor**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
python -m pytest tests/entity/ --cov=src --cov-report=html
start htmlcov\index.html
```

---

**User**

`htmlcov` 폴더가 안 생김.

---

**Cursor**

**원인:** `tests/boundary/` 수집 ERROR → pytest 세션 중단 → cov HTML 미생성.

**해결:**

```powershell
python -m pytest tests/entity/ --cov=src --cov-report=html
# 또는
python -m pytest --ignore=tests/boundary --cov=src --cov-report=html
```

---

**User**

[P] QA. 결함을 `defect_list.md`에 정리. README 결함 체크박스 업데이트.

---

**Cursor**

`defect_list.md` — DEF-001~006 (boundary 미구현, SSOT drift, resolve vs solve_partial_grid, htmlcov, 레이어 미착수, DT 미착수).

README: `[x] defect_list.md 생성`

---

**User**

Report 폴더 보고서 + Prompting Transcript Export + README 현재 상태 갱신.

---

**Cursor**

- `Report/08-test-plan-red-phase-report.md`
- `Prompting/08-test-plan-red-phase-prompt.md` (본 문서)
- `README.md` — 구조·문서·진행·로컬 실행 갱신

---

## 재사용 프롬프트 (테스트 플랜·RED 일괄)

```markdown
Magic Square 4×4 — AC-FR01-01 RED 착수

Phase A — 샘플 AC 선정 (코드 금지)
- FR-01 NULL 선행, Boundary·Domain 0-call
- 출력: AC-FR01-01, ERR_NULL_GRID, UT-01

Phase B — test_plan.md (QA Lead)
- P0 UT-01, P1 UT-02~03, mock/spy, cov 95/85/80
- Python 3.10+

Phase C — README RED To-Do (PRD SSOT)

Phase D — tests/boundary RED (5 tests, pytest FAIL)
- Red 없이 src/ 추가 금지 → Green 시 boundary/entry.py

Phase E — defect_list.md + Report/08 + Prompting/08

SSOT: Report/02 Error message, PRD §13.1
```

---

## 관련 문서

| 문서 | 경로 |
|------|------|
| 본 단계 보고서 | `Report/08-test-plan-red-phase-report.md` |
| 테스트 플랜 | `docs/test_plan.md` |
| 결함 목록 | `defect_list.md` |
| TDD 설계 | `Report/02-tdd-design-report.md` |
