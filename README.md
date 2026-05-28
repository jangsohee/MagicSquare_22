# MagicSquare_

4×4 마방진을 다루는 학습·실험 프로젝트입니다.  
Cursor AI와 협업하며 **문제 정의 → 규칙 고정 → PRD → 검증 가능한 구현** 순서로 개발 역량을 기릅니다.

> **현재 단계:** 구현 전 **PRD** 확정(`docs/PRD_MagicSquare.md`) · User Journey(Report/06) · Cursor Rules 5파일 · User Entity 1차 구현 · 마방진 핵심(DT-01) **착수 전**

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
│   └── PRD_MagicSquare.md                 # 구현 전 PRD (v1.0 Draft)
├── README.md
├── pyproject.toml                         # pytest · black · ruff
├── src/magicsquare/                       # Python ECB
│   ├── entity/                            # Domain (User Entity 구현됨)
│   ├── boundary/                          # I/O 검증·응답 (예정)
│   ├── control/                           # Use case (예정)
│   └── data/                              # Repository (예정)
├── tests/
│   ├── entity/                            # test_user.py (9 passed)
│   ├── boundary/ · data/ · integration/   # (예정)
│   └── conftest.py                        # (예정)
├── Report/
│   ├── 01-problem-definition-report.md
│   ├── 02-tdd-design-report.md            # 계약·TC-ID SSOT
│   ├── 03-cursor-rules-and-implementation-report.md
│   ├── 04-magicsquare-rules-consolidation-report.md
│   ├── 05-cursor-agents-prompt-set-report.md
│   ├── 06-user-journey-to-scenario-verification-report.md
│   └── 07-prd-creation-and-review-report.md
└── Prompting/
    ├── 01-problem-definition-prompt.md
    ├── 02-tdd-design-prompt.md
    ├── 03-cursor-rules-implementation-prompt.md
    ├── 04-magicsquare-rules-consolidation-prompt.md
    ├── 05-cursor-agents-prompt-set-prompt.md
    ├── 06-user-journey-to-scenario-verification-prompt.md
    └── 07-prd-creation-and-review-prompt.md
```

---

## 문서

### 핵심 (구현 착수 시)

| 문서 | 설명 |
|------|------|
| [**PRD**](docs/PRD_MagicSquare.md) | 구현 전 기준 — FR, BR, I/O·Error 계약, Dual-Track, Traceability |
| [TDD 설계 보고서](Report/02-tdd-design-report.md) | TC-ID·Error message·Invariant **단일 진실 원천** |
| [User Journey 보고서](Report/06-user-journey-to-scenario-verification-report.md) | Epic → Story → Scenario → Verification |
| [PRD 작성·검토 보고서](Report/07-prd-creation-and-review-report.md) | PRD 산출·7항목 검토·P0~P2 개선 권장 |

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
- [ ] DEC-01: ECB 레이어 배치 확정 (Report/02 ↔ PRD)
- [ ] PRD v1.1 (AC-ID Matrix, Layer 용어 통일)
- [ ] Mom Test · 1차 사용자 확정
- [ ] Domain Track: **DT-01** Red부터
- [ ] UI Track: **UT-04** Red부터 (병행)
- [ ] Data Track · 통합 테스트 (IT-OK / IT-FAIL)

---

## 미해결 항목

- **1차 사용자** — Mom Test 미완 (PRD Persona: TDD 학습자로 가정)
- **ECB harmonization** — PRD §22 DEC-01 (Judge/Solver → entity vs control)
- **PRD 검토 보완** — AC-ID 전수 Traceability, DT-07/12 AC (Report/07 P0~P1)
- **`pytest-cov` CI** — 커버리지 gate 미구성

---

## 로컬 실행

```bash
pip install -e ".[dev]"
pytest
```

---

## 방법론 참고

- **The Mom Test** — 가설이 아닌 관찰
- **5 Whys** — 표면 요구에서 구조적 불편 도출
- **Dual-Track TDD** — Boundary(UT-*) ∥ Domain(DT-*), Red → Green → Refactor

---

## 라이선스

미정
