# Magic Square 4×4 — 테스트 계획서 (Test Plan)

| Field | Value |
|---|---|
| **Document ID** | TP-MSQ-FR01-001 |
| **Version** | 1.0 |
| **Status** | Pre-implementation baseline |
| **Author Role** | Senior QA Lead |
| **Anchor AC** | **AC-FR01-01** (`grid is null` → `ERR_NULL_GRID`, Domain 0회) |
| **Primary SSOT** | `Report/02-tdd-design-report.md`, `docs/PRD_MagicSquare.md` §10·§13·§15·§16 |
| **Stack** | Python 3.10+, pytest, pydantic (응답 envelope), unittest.mock |
| **Target Path** | `tests/boundary/` (Track A), `tests/integration/` (IT-FAIL-01) |

---

## 1. Executive Summary

본 계획서는 **선택 샘플 AC-FR01-01**(`grid = None`)을 **P0 앵커**로, FR-01 Boundary 입력 검증의 **선행·단락(short-circuit)** 동작과 **Domain 진입점 격리(BR-15)** 를 pytest 기반으로 검증한다.

계약상 `grid = None`의 Error code는 **`ERR_NULL_GRID`** 이며, message는 **`Input grid is null.`** 이다.  
(요청 서식 예시의 `INVALID_SIZE` / `"Grid must be 4x4."`는 **크기 불일치** 계열 `ERR_GRID_ROWS` / `ERR_GRID_COLS`에 해당하며, AC-FR01-01 범위 밖이다.)

**검증 순서(고정):** `NULL → ROWS → COLS → RANGE → EMPTY_COUNT → DUPLICATE`  
**첫 위반 1건만** 반환하며, Boundary 실패 시 `solve_partial_grid` 등 Domain resolver는 **0회** 호출된다.

---

## 2. Scope

### 2.1 In-Scope (본 계획 1차 스프린트)

| Layer | Component | Test Path | TC-ID |
|---|---|---|---|
| Boundary | `BoundaryValidator`, `ErrorFactory`, `ResponseMapper` | `tests/boundary/` | UT-01 (P0), UT-02~03 (P1) |
| Integration | Boundary → Control 진입 (실 Domain, Mock 금지) | `tests/integration/` | IT-FAIL-01 (P1) |

### 2.2 Out-of-Scope (AC-FR01-01 범위 외 — 본 계획에 포함 금지)

| Input | Reason | Deferred TC |
|---|---|---|
| **4×4 정상 격자** (예: G_PARTIAL_FWD) | AC-FR01-01은 null 단락만 대상; 성공·Domain 1회 호출은 AC-FR01-07 / UT-09 영역 | UT-09, IT-OK-01 |
| RANGE / EMPTY_COUNT / DUPLICATE 위반 | NULL·SIZE 선행 검증 완료 후 별도 스프린트 | UT-04~08 |
| Domain 불변식·Solver | Track B (entity/control) | DT-01~ |

---

## 3. Test Objectives

1. **Contract:** `grid = None` → `status="ERROR"`, `code="ERR_NULL_GRID"`, `message="Input grid is null."` (**바이트 동일**)
2. **Isolation:** invalid input 시 Domain resolver **`solve_partial_grid` 호출 0회** (BR-15, NFR-11)
3. **Short-circuit:** null 입력에서 ROWS/COLS 이후 검증 분기 **미진입** (spy/라인 커버리지로 간접 확인)
4. **Regression:** FR-01 크기 불일치 경계값(UT-02, UT-03)을 P1로 병행 — Dual-Track 교차 진행 원칙 준수

---

## 4. pytest 단위 테스트 범위 및 우선순위

### 4.1 Priority Matrix

| Priority | TC-ID | AC | Scenario | Assert Focus | Mock Policy |
|---|---|---|---|---|---|
| **P0** | **UT-01** | AC-FR01-01 | `grid = None` | ERROR envelope + message exact + Domain **0회** | `solve_partial_grid` Mock/spy |
| **P1** | UT-02 | AC-FR01-02 | `grid = []`, 3×4, 5×5 | `ERR_GRID_ROWS`, Domain 0회 | Mock/spy |
| **P1** | UT-03 | AC-FR01-03 | `grid = [[]]*4`, 4×3 | `ERR_GRID_COLS`, Domain 0회 | Mock/spy |
| **P1** | IT-FAIL-01 | AC-FR01-01~06 | invalid input E2E | 실 Boundary + 실 Control/Entity, Domain solve **0회** | **Mock 금지** |
| **P2** | UT-04~08 | AC-FR01-04~06 | 값·빈칸·중복 | 각 Error code/message | Mock/spy |
| **P2** | UT-09 | AC-FR01-07 | 유효 4×4 | Domain **1회**, OK result | Mock 반환값 주입 |
| **—** | *(제외)* | — | 4×4 정상 입력 | AC-FR01-01 범위 외 | — |

### 4.2 Recommended RED Order (Report/06 · PRD §15.1)

```
P0: UT-01 (null)
P1: UT-02 (rows) ∥ UT-03 (cols)   ← 병렬 가능
P1: IT-FAIL-01 (integration guard)
P2: UT-06 → UT-08 → UT-04         ← FR-01 나머지
```

### 4.3 Test Naming & Structure

- **파일:** `tests/boundary/test_ut01_null_grid.py` (TC-ID 1 Red = 1 파일 권장)
- **함수:** `test_ut01_null_grid_returns_err_null_grid_and_skips_domain`
- **패턴:** AAA (Arrange / Act / Assert)
- **금지:** Red 없이 `src/` 추가, assert 완화, `skip`/`xfail`, integration에서 Domain Mock

### 4.4 Optional: pydantic Envelope 검증

Boundary 응답 DTO가 pydantic `BaseModel`일 경우, 테스트에서 **Act 직후** `ErrorResponse.model_validate(result)`로 schema drift를 조기 탐지한다.  
message/code assert는 여전히 **Report/02 고정 문자열**과 완전 일치를 기준으로 한다.

---

## 5. 경계값 케이스 목록

검증 순서에 따라 **기대 Error code**가 달라진다. AC-FR01-01 앵커는 **첫 행(P0)** 만 해당한다.

| ID | Input (`grid`) | Expected `code` | Expected `message` | AC | TC-ID | Priority | AC-FR01-01 범위 |
|---|---|---|---|---|---|---|---|
| **BV-01** | `None` | `ERR_NULL_GRID` | `Input grid is null.` | AC-FR01-01 | UT-01 | **P0** | **In** |
| BV-02 | `[]` (빈 리스트, row=0) | `ERR_GRID_ROWS` | `Grid must have exactly 4 rows.` | AC-FR01-02 | UT-02 | P1 | Out |
| BV-03 | `[[]] * 4` (행 4, 열 0) | `ERR_GRID_COLS` | `Each row must have exactly 4 columns.` | AC-FR01-03 | UT-03 | P1 | Out |
| BV-04 | 3×4 (행 3, 열 4) | `ERR_GRID_ROWS` | `Grid must have exactly 4 rows.` | AC-FR01-02 | UT-02 | P1 | Out |
| BV-05 | 4×3 (행 4, 열 3) | `ERR_GRID_COLS` | `Each row must have exactly 4 columns.` | AC-FR01-03 | UT-03 | P1 | Out |
| BV-06 | 5×5 | `ERR_GRID_ROWS` | `Grid must have exactly 4 rows.` | AC-FR01-02 | UT-02 | P1 | Out |
| **BV-07** | 4×4 정상 격자 (G_PARTIAL_FWD 등) | `OK` / `result` | — | AC-FR01-07 | UT-09 | — | **포함 금지** |

### 5.1 BV-01 (P0) 상세 — AC-FR01-01

| Item | Specification |
|---|---|
| **Given** | `grid = None` |
| **When** | Boundary 진입점 호출 (예: `validate_and_solve(grid)` 또는 `BoundaryValidator.validate(grid)`) |
| **Then** | `{ "status": "ERROR", "code": "ERR_NULL_GRID", "message": "Input grid is null." }` |
| **And** | `solve_partial_grid` **call_count == 0** |
| **And** | `result` 필드 **없음** (ERROR envelope) |

### 5.2 Short-Circuit 검증 (BV-01 부가)

null 입력 시 **ROWS/COLS 분기 미실행**을 다음 중 하나로 확인:

- Mock/spy: row/col 검사 헬퍼가 있다면 `assert not called`
- Coverage: `BoundaryValidator` null 분기 hit, rows/cols 분기 miss (UT-01 단독 실행 시)

---

## 6. 예외 / 특이 케이스 목록

| ID | Category | Scenario | Expected Behavior | TC | Notes |
|---|---|---|---|---|---|
| **EX-01** | Null semantics | 명시적 `None` 전달 | `ERR_NULL_GRID`, Domain 0 | UT-01 | Python `None` ≡ PRD `null` |
| EX-02 | Type abuse | `grid = "not a list"` | 구현 전략에 따름 — **권장:** ROWS 검사에서 `ERR_GRID_ROWS` 또는 타입 가드 Error | *(backlog)* | pydantic 입력 모델 사용 시 사전 차단 가능 |
| EX-03 | Type abuse | `grid = 123` (스칼라) | ROWS 불일치로 단락 | *(backlog)* | |
| EX-04 | Jagged row | `[[1,2,3,4],[1,2],[1,2,3,4],[1,2,3,4]]` | `ERR_GRID_COLS` (첫 jagged row) | UT-03 변형 | P1 확장 |
| EX-05 | First violation | null + 잘못된 크기 동시 해당 불가 | null **우선** — BV-01만 발화 | UT-01 | 검증 순서 invariant |
| EX-06 | Message freeze | message 부분 일치 assert | **FAIL** — 완전 문자열 일치만 허용 | UT-01~08 | NFR-09, REG-02 |
| EX-07 | Uncaught exception | Boundary가 Exception 전파 | **FAIL** — ERROR envelope 반환 필수 | UT-01 | §13.2 Domain failure와 구분 |
| EX-08 | Integration | IT 경로에서 invalid blank | Domain solve 0회 | IT-FAIL-01 | Mock 금지 |
| EX-09 | `[[]]*4` aliasing | 4행 동일 빈 row 객체 참조 | `ERR_GRID_COLS` (열 0) | UT-03 | Python list 곱셈 함정 |

---

## 7. Domain resolver 호출 횟수 검증 전략 (Mock / Spy)

### 7.1 원칙 (PRD §15.1, NFR-11)

| Track | Domain Mock | Assert |
|---|---|---|
| **Track A** (`tests/boundary/`) | **허용** — `unittest.mock.patch` / `MagicMock` | invalid → **0회**, valid → **1회** (UT-09) |
| **Integration** (`tests/integration/`) | **금지** | invalid → solve 경로 **0회** (행위·결과로 검증) |

### 7.2 Track A — UT-01 (P0) 권장 패턴

**대상:** `magicsquare.control.<module>.solve_partial_grid` (또는 Boundary가 주입받는 resolver port)

**전략 A — `@patch` + call_count (권장)**

```python
@patch("magicsquare.boundary.<entry>.solve_partial_grid")
def test_ut01_null_grid_returns_err_null_grid_and_skips_domain(mock_solve):
    # Arrange
    grid = None

    # Act
    response = validate_and_solve(grid)

    # Assert — contract
    assert response.status == "ERROR"
    assert response.code == "ERR_NULL_GRID"
    assert response.message == "Input grid is null."

    # Assert — isolation
    mock_solve.assert_not_called()
```

**전략 B — Spy (wraps 실함수, UT-01에서는 A로 충분)**

- `@patch(..., wraps=solve_partial_grid)` — valid path(UT-09)에서 side effect + call_count 동시 검증 시 유용
- **UT-01(null):** spy 불필요; Mock이 더 명확

**전략 C — pytest fixture (conftest)**

```python
@pytest.fixture
def mock_solve_partial_grid(mocker):
    return mocker.patch(
        "magicsquare.boundary.<entry>.solve_partial_grid",
        autospec=True,
    )
```

- `autospec=True` → 잘못된 시그니처 조기 발견
- fixture teardown 자동

### 7.3 Integration — IT-FAIL-01

| Approach | Description |
|---|---|
| **행위 기반** | invalid grid → ERROR code + **실제 Domain side effect 없음** (파일/로그/내부 상태 변경 없음) |
| **간접 카운트** | Control에 `@dataclass` call counter (테스트 전용 hook) — **프로덕션 오염 금지**, port injection 선호 |
| **결과 기반** | `ERR_NULL_GRID` + 응답 시간/부수 효과 — solve 연산 characteristic 미발생 |

### 7.4 Anti-Patterns (금지)

- Integration 테스트에서 `solve_partial_grid` Mock → NFR-10 위반
- `assert mock_solve.call_count <= 1` 같은 완화 assert
- Domain Mock 없이 Boundary만 단독 테스트하고 IT-FAIL-01 생략

---

## 8. 커버리지 목표

| Layer / Package | Target | Rationale | Primary TC |
|---|---|---|---|
| **Domain** (`entity`, `control` domain logic) | **≥ 95%** line | NFR-01, PRD §14 | DT-01~ (Track B) |
| **Boundary** (`boundary` validator + response) | **≥ 85%** line | NFR-02 | UT-01~08 |
| **Data** (optional) | **≥ 80%** line | NFR-03 | ST-01~ |
| **Overall** (`src/`) | **≥ 80%** line | Engineering §20 | UT + DT + IT |

### 8.1 AC-FR01-01 스프린트별 기대 커버리지

| Milestone | Boundary | Domain | Comment |
|---|---|---|---|
| **M1: UT-01 Green** | null 분기 hit | 변화 없음 (0-call) | Domain 미호출이므로 Domain %는 Track B에 의존 |
| **M2: UT-01~03 Green** | NULL+ROWS+COLS path | — | Boundary ≥40% 예상 (전체 UT-08 전 ~85%) |
| **M3: UT-01~08 + IT-FAIL-01** | **≥ 85%** | Track B 병행 시 **≥ 95%** | Dual-Track exit criteria |

### 8.2 Coverage Exclusions (명시적)

- `if TYPE_CHECKING:` 블록
- `pragma: no cover` — **사용 금지** (커버리지 목표 우회 방지)
- 테스트 전용 hook 코드 — 가능하면 `tests/`에만 배치

---

## 9. pytest-cov 측정 전략

### 9.1 설치

```bash
pip install pytest-cov
```

*(프로젝트에 `pyproject.toml` / `requirements-dev.txt`가 생기면 dev dependency로 고정)*

### 9.2 기본 측정 (전체)

```bash
pytest --cov=src --cov-report=term-missing
```

### 9.3 레이어별 측정 (QA Gate)

**Boundary only (Track A 스프린트)**

```bash
pytest tests/boundary/ \
  --cov=src/magicsquare/boundary \
  --cov-report=term-missing \
  --cov-fail-under=85
```

**Domain only (Track B)**

```bash
pytest tests/entity/ tests/control/ \
  --cov=src/magicsquare/entity \
  --cov=src/magicsquare/control \
  --cov-report=term-missing \
  --cov-fail-under=95
```

**P0 단독 (UT-01 Red→Green 확인)**

```bash
pytest tests/boundary/test_ut01_null_grid.py -v \
  --cov=src/magicsquare/boundary \
  --cov-report=term-missing
```

### 9.4 CI / Local Gate 권장

| Gate | Command | Threshold |
|---|---|---|
| PR — Boundary 변경 | `pytest tests/boundary/ --cov=... --cov-fail-under=85` | 85% |
| PR — Domain 변경 | `pytest tests/entity/ tests/control/ --cov-fail-under=95` | 95% |
| Nightly | `pytest --cov=src --cov-report=html --cov-fail-under=80` | 80% overall |

### 9.5 Coverage 해석 가이드 (QA Lead)

- **UT-01만 Green:** Boundary null 분기 1 path — **85% 미달 정상**; UT-02~08로 수렴
- **Domain 95%:** UT-01은 Domain line을 실행하지 않음 → **DT 시리즈 필수**
- **`term-missing`:** 미커버 라인을 TC backlog에 매핑 (예: `validator.py:42` → UT-02)

---

## 10. Test Data & Fixtures

| Fixture ID | Location | Content | Used By |
|---|---|---|---|
| `NULL_GRID` | inline | `None` | UT-01, IT-FAIL-01 |
| `EMPTY_LIST_GRID` | inline | `[]` | UT-02 |
| `FOUR_EMPTY_ROWS` | inline | `[[]] * 4` | UT-03 |
| `G_INVALID_ROWS` | `conftest.py` / PRD §12.4 | 3×4 | UT-02 |
| `G_PARTIAL_FWD` | `conftest.py` | 4×4 valid | **UT-09 only — 본 계획 제외** |

---

## 11. Exit Criteria (AC-FR01-01 스프린트)

- [ ] **UT-01** Red → pytest FAIL 확인 → Green → PASS
- [ ] `grid=None` → `ERR_NULL_GRID`, message **완전 일치**
- [ ] `solve_partial_grid` Mock **`assert_not_called()`** PASS
- [ ] BV-02~06 (P1) UT-02/03 backlog 등록 또는 PASS
- [ ] BV-07 (4×4 정상) **본 스프린트 테스트 suite에 미포함** 확인
- [ ] Boundary `--cov-fail-under=85` — UT-01~03만으로는 미달 가능; 전체 UT-08 완료 시 PASS
- [ ] IT-FAIL-01 (P1) — 실 Domain Mock 없이 invalid → ERROR + no solve

---

## 12. Traceability

| Concept | Business Rule | FR | AC | Test Case | Component |
|---|---|---|---|---|---|
| Null grid rejection | — | FR-01 | AC-FR01-01 | **UT-01**, IT-FAIL-01 | BoundaryValidator |
| Domain 0-call on invalid | BR-15 | FR-01 | AC-FR01-01~06 | UT-01~08 | BoundaryValidator |
| Error message frozen | — | FR-01 | AC-FR01-* | UT-01~08 | ErrorFactory |
| 4×4 row count | BR-01 | FR-01 | AC-FR01-02 | UT-02 | BoundaryValidator |
| 4×4 col count | BR-01 | FR-01 | AC-FR01-03 | UT-03 | BoundaryValidator |

---

## 13. References

| Document | Path |
|---|---|
| PRD | `docs/PRD_MagicSquare.md` |
| Design / Contract / TC-ID | `Report/02-tdd-design-report.md` |
| User Journey / Scenario | `Report/06-user-journey-to-scenario-verification-report.md` |
| TDD Rules | `.cursor/rules/magicsquare-tdd-testing.mdc` |

---

*End of Test Plan — TP-MSQ-FR01-001*
