# MagicSquare_

4×4 마방진을 다루는 학습·실험 프로젝트입니다.  
Cursor AI와 협업하며 **문제 정의 → 규칙 고정 → PRD → 검증 가능한 구현** 순서로 개발 역량을 기릅니다.

> **현재 단계:** **RED** — AC-FR01-01 / UT-01 Boundary 테스트 작성 완료 · `test_plan.md` · `defect_list.md` (DEF-001~006 Open) · Boundary **Green 미착수** (`magicsquare.boundary` 없음) · Entity **9 passed**

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
├── defect_list.md                         # 결함 DEF-001~006 (Open)
├── README.md
├── pyproject.toml                         # pytest · pytest-cov · pydantic · black · ruff
├── .venv/                                 # 로컬 가상환경 (gitignore)
├── src/magicsquare/                       # Python ECB
│   ├── entity/                            # User Entity 구현됨
│   ├── boundary/                          # (미구현 — RED 원인)
│   ├── control/                           # (예정)
│   └── data/                              # (예정)
├── tests/
│   ├── entity/test_user.py                # 9 passed
│   ├── boundary/test_ac_fr01_01_null_grid.py  # RED — 수집 ERROR
│   └── data/ · integration/               # (예정)
├── Report/
│   ├── 01-problem-definition-report.md
│   ├── 02-tdd-design-report.md            # 계약·TC-ID SSOT
│   ├── 03-cursor-rules-and-implementation-report.md
│   ├── 04-magicsquare-rules-consolidation-report.md
│   ├── 05-cursor-agents-prompt-set-report.md
│   ├── 06-user-journey-to-scenario-verification-report.md
│   ├── 07-prd-creation-and-review-report.md
│   └── 08-test-plan-red-phase-report.md   # test_plan · RED · QA
└── Prompting/
    ├── 01-problem-definition-prompt.md
    ├── 02-tdd-design-prompt.md
    ├── 03-cursor-rules-implementation-prompt.md
    ├── 04-magicsquare-rules-consolidation-prompt.md
    ├── 05-cursor-agents-prompt-set-prompt.md
    ├── 06-user-journey-to-scenario-verification-prompt.md
    ├── 07-prd-creation-and-review-prompt.md
    └── 08-test-plan-red-phase-prompt.md
```

---

## 문서

### 핵심 (구현 착수 시)

| 문서 | 설명 |
|------|------|
| [**PRD**](docs/PRD_MagicSquare.md) | 구현 전 기준 — FR, BR, I/O·Error 계약, Dual-Track, Traceability |
| [**테스트 플랜**](docs/test_plan.md) | AC-FR01-01 앵커 · UT-01~08 · pytest-cov 전략 |
| [**결함 목록**](defect_list.md) | DEF-001~006 (RED 단계 Open) |
| [TDD 설계 보고서](Report/02-tdd-design-report.md) | TC-ID·Error message·Invariant **단일 진실 원천** |
| [User Journey 보고서](Report/06-user-journey-to-scenario-verification-report.md) | Epic → Story → Scenario → Verification |
| [PRD 작성·검토 보고서](Report/07-prd-creation-and-review-report.md) | PRD 산출·7항목 검토·P0~P2 개선 권장 |
| [테스트 플랜·RED·QA 보고서](Report/08-test-plan-red-phase-report.md) | test_plan · boundary RED · defect_list · 커버리지 이슈 |

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
- [x] **UT-01 RED** — `tests/boundary/test_ac_fr01_01_null_grid.py` (5 tests, 수집 ERROR = 의도된 RED)
- [x] **결함 목록** (`defect_list.md`, DEF-001~006)
- [ ] **UT-01 Green** — `src/magicsquare/boundary/` 최소 구현 (DEF-001)
- [ ] RED 테스트 ↔ PRD SSOT 정렬 (`ERR_NULL_GRID`, `solve_partial_grid` — DEF-002·003)
- [ ] DEC-01: ECB 레이어 배치 확정 (Report/02 ↔ PRD)
- [ ] PRD v1.1 (AC-ID Matrix, Layer 용어 통일)
- [ ] Mom Test · 1차 사용자 확정
- [ ] Domain Track: **DT-01** Red (병행)
- [ ] UI Track: **UT-02~08** Red (P1)
- [ ] Data Track · 통합 테스트 (IT-OK / IT-FAIL)

---

## RED 단계 To-Do 리스트

> 이 체크리스트는 [test_plan.md](docs/test_plan.md) 기반 — **AC-FR01-01** (`grid=None` → `ERR_NULL_GRID`, UT-01) 앵커.
> 각 항목은 RED(실패 테스트 작성) 완료 시 체크합니다.

### Track A — UI / Boundary 테스트 (P0: AC-FR01-01 / UT-01)
- [ ] TC-A-01: grid=None 입력 → status="ERROR" 실패 결과 반환
- [ ] TC-A-02: code가 정확히 `"ERR_NULL_GRID"` 문자열인지 검증
- [ ] TC-A-03: message가 `"Input grid is null."` 과 문자 단위 동일한지 검증
- [ ] TC-A-04: grid=None 시 Domain 진입점(`solve_partial_grid`) 0회 호출 (mock/spy 검증)
- [ ] TC-A-07: 반환 객체 타입이 지정 ERROR envelope 구조체인지 검증

### Track A — P1 확장 (AC-FR01-02·03 / UT-02·03)
- [ ] TC-A-05: grid=[] 빈 리스트 → `ERR_GRID_ROWS`, Domain 0회
- [ ] TC-A-06: grid=3×4 크기 불일치 → `ERR_GRID_ROWS`, Domain 0회

### Track B — Domain / Logic 테스트 (격리)
- [ ] TC-B-01: `solve_partial_grid`가 None grid를 직접 받지 않음을 격리 검증
- [ ] TC-B-02: Boundary가 None 분기 처리 후 `solve_partial_grid` 미호출 확인
- [ ] TC-B-03: `solve_partial_grid` mock이 호출됐을 경우 테스트 실패 처리
- [ ] TC-B-04: AC-FR01-02~06 범위 케이스는 AC-FR01-01 RED 커밋에 포함하지 않음 확인

### 커버리지 목표
- [ ] Domain Logic: 95%+ (`pip install pytest-cov`)
- [ ] Boundary Layer: 85%+
- [ ] 전체 TOTAL: 80%+

### 결함 목록 연결
- [x] [defect_list.md](defect_list.md) 생성 및 발견 결함 기록 (DEF-001~006)
- [ ] 모든 결함 수정 후 회귀 테스트 통과 확인

---

## 미해결 항목

- **1차 사용자** — Mom Test 미완 (PRD Persona: TDD 학습자로 가정)
- **ECB harmonization** — PRD §22 DEC-01 (Judge/Solver → entity vs control)
- **PRD 검토 보완** — AC-ID 전수 Traceability, DT-07/12 AC (Report/07 P0~P1)
- **`pytest-cov` CI** — 커버리지 gate 미구성
- **RED 테스트 계약 drift** — boundary 테스트 `INVALID_SIZE` vs PRD `ERR_NULL_GRID` (DEF-002)

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
# Entity만 (9 passed)
python -m pytest tests/entity/ -v

# 전체 (boundary 수집 ERROR — RED)
python -m pytest -v

# Boundary RED만
python -m pytest tests/boundary/ -v
```

### 커버리지 HTML

```powershell
# boundary 제외 시 htmlcov 생성
python -m pytest tests/entity/ --cov=src --cov-report=html
start htmlcov\index.html

# 또는
python -m pytest --ignore=tests/boundary --cov=src --cov-report=html
```

> 전체 `pytest --cov=src --cov-report=html` 은 boundary 수집 실패 시 `htmlcov/`가 생기지 않을 수 있음 ([DEF-004](defect_list.md)).

---

## 방법론 참고

- **The Mom Test** — 가설이 아닌 관찰
- **5 Whys** — 표면 요구에서 구조적 불편 도출
- **Dual-Track TDD** — Boundary(UT-*) ∥ Domain(DT-*), Red → Green → Refactor

---

## 라이선스

미정
