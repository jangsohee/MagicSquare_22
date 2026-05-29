# Magic Square 프로젝트 — Cursor Agent 프롬프트 세트 보고서

**작성 목적:** MagicSquare 4×4 TDD 연습용 **역할별 Cursor Agent 8종** 프롬프트 설계·생성·정리 결과 정리  
**대상:** 주니어 개발자 + Cursor AI 협업 학습 프로젝트  
**범위:** `.cursor/agents/*.md` 8파일 · 레거시 Agent 정리 · Report/Prompting Export  
**선행 문서:** `Report/04-magicsquare-rules-consolidation-report.md`, `Report/02-tdd-design-report.md`  
**작성일:** 2026-05-28

---

## Executive Summary

본 단계에서 MagicSquare 프로젝트는 **Dual-Track TDD · ECB · Report/02 계약**에 정합된 **공식 Cursor Agent 8종**을 정의하고 `.cursor/agents/`에 배치했다. 초기에는 텍스트만 출력했으나, 이후 파일 생성·레거시 Agent 정리까지 완료했다.

| 산출물 | 상태 |
|--------|------|
| `.cursor/agents/` 공식 Agent 8파일 | **완료** |
| 레거시 Agent 6파일 삭제 | **완료** |
| `Report/05` (본 문서) | **완료** |
| `Prompting/05` Transcript Export | **완료** |
| `src/` 마방진 핵심 (DT-01~) | 미착수 (변경 없음) |

**pytest:** `9 passed` (변경 없음 — `tests/entity/test_user.py`)

---

## STEP 1 — 요청 배경

### 1.1 목표

- MagicSquare 4×4 TDD 연습에서 **역할 분리**된 Cursor Agent 프롬프트 세트 구축
- 각 Agent가 **Report/02 계약**, **ECB 레이어**, **Dual-Track TDD(Red→Green→Refactor)** 를 공통으로 준수
- Agent별 **저장 경로 · Role · Responsibilities · Workflow · Must Not · Output Format** 통일

### 1.2 제약 (요청 시 고정)

- 1차: **파일 생성 없이** 복사 가능 텍스트만 출력
- 2차: `.cursor/agents/<agent-name>.md` 로 **실제 파일 생성**
- 3차: **레거시 Agent 정리** (공식 8개만 유지)
- 4차: **Report · Prompting Export**

---

## STEP 2 — Agent 프롬프트 설계

### 2.1 공통 프롬프트 구조

모든 Agent는 아래 섹션을 따른다.

| 섹션 | 내용 |
|------|------|
| YAML frontmatter | `name`, `description`, `model: inherit`, `readonly` |
| 저장 경로 | `.cursor/agents/<agent-name>.md` |
| Agent Name | 영문 역할명 |
| Role | MagicSquare 맥락에서의 역할 한 줄 |
| Responsibilities | 책임 목록 |
| Workflow | 작업 절차 (7단계 내외) |
| Must Not | 공통 안전 규칙 + 역할별 금지 |
| Output Format | 보고 템플릿 (markdown) |
| 참고 | Report/02, `.cursor/rules/magicsquare-*.mdc` |

### 2.2 공통 안전·TDD 규칙 (전 Agent)

- 사용자 승인 없이 push·삭제·배포·DB 변경 금지
- secret 출력·커밋 금지
- Red 없이 `src/` 프로덕션 추가 금지
- 테스트 약화·skip/xfail 금지
- ECB 경계 준수 (boundary→control→entity)
- type hints + Google docstring, PEP8, `logging` (no `print`)
- UI/Boundary RED vs Logic/Domain RED 분리
- 입력 검증 계약과 마방진 해결 로직 혼합 금지

### 2.3 MagicSquare 도메인 (Agent 공통 참조)

| 항목 | 값 |
|------|-----|
| 입력 | 4×4 `int[][]`, `0`=빈칸(정확히 2개), 값 `0` 또는 `1~16`, 0 제외 중복 금지 |
| 출력 | `int[6]` = `[r1,c1,n1,r2,c2,n2]`, 좌표 **1-index** |
| Magic Constant | **34** (행·열·주대각·부대각 10선) |
| 배치 규칙 | 작은 누락 수→첫 빈칸, 큰 수→둘째 빈칸이 magic이면 그 순서, 아니면 반대 |
| Boundary 검증 순서 | `NULL → ROWS → COLS → RANGE → EMPTY_COUNT → DUPLICATE` |

---

## STEP 3 — 공식 Agent 8종

| # | 파일 | Agent Name | readonly | 주요 책임 |
|---|------|------------|----------|-----------|
| 1 | `system-optimization-engineer.md` | System Optimization Engineer | false | 병목 측정·성능 개선 (계약·behavior 불변) |
| 2 | `ux-design-advisor.md` | UX Design Advisor | false | 입력·결과·에러 UX, 접근성 (§2.2 message 본문 변경 금지) |
| 3 | `product-planning-manager.md` | Product Planning Manager | **true** | PRD, 범위·마일스톤, TC-ID 매핑 |
| 4 | `backend-developer.md` | Backend Developer | false | ECB boundary/control/entity/data, Dual-Track TDD 구현 |
| 5 | `frontend-developer.md` | Frontend Developer | false | 4×4 UI, API 연동, presentation (domain 로직 금지) |
| 6 | `quality-assurance-engineer.md` | Quality Assurance Engineer | **true** | TC-ID·계약·회귀·커버리지 검증, 버그 위임 |
| 7 | `ai-integration-expert.md` | AI Integration Expert | false | LLM adapter/port (domain invariant LLM 위임 금지) |
| 8 | `backup-report-github-manager.md` | Backup Report GitHub Manager | false | Report/Prompting, Git·PR·백업 (push는 승인 후) |

### 3.1 Agent 협업 매트릭스

```
product-planning-manager (PRD)
        │
        ├── backend-developer ──┬── quality-assurance-engineer
        ├── frontend-developer ─┤
        ├── ux-design-advisor ──┘
        ├── system-optimization-engineer
        ├── ai-integration-expert
        └── backup-report-github-manager (문서·Git)
```

| readonly Agent | 코드 수정 | 위임 대상 |
|----------------|-----------|-----------|
| product-planning-manager | 불가 | backend, frontend, qa |
| quality-assurance-engineer | 불가 | backend, frontend, ux |

---

## STEP 4 — 파일 생성·갱신 (Turn 2)

### 4.1 생성·갱신된 파일 (8개)

| 동작 | 경로 |
|------|------|
| 생성 | `.cursor/agents/system-optimization-engineer.md` |
| 생성 | `.cursor/agents/product-planning-manager.md` |
| 생성 | `.cursor/agents/quality-assurance-engineer.md` |
| 생성 | `.cursor/agents/ai-integration-expert.md` |
| 생성 | `.cursor/agents/backup-report-github-manager.md` |
| 갱신 | `.cursor/agents/ux-design-advisor.md` |
| 갱신 | `.cursor/agents/backend-developer.md` |
| 갱신 | `.cursor/agents/frontend-developer.md` |

### 4.2 참조한 선행 자료

- `.cursorrules` — ECB, Dual-Track TDD, forbidden
- `Report/02-tdd-design-report.md` — I/O 계약, invariant, TC-ID
- 기존 `.cursor/agents/` 초안 (backend, ux, qa, performance-optimizer 등)

---

## STEP 5 — 레거시 Agent 정리 (Turn 3)

### 5.1 삭제한 파일 (6개)

| 삭제 파일 | 대체·사유 |
|-----------|-----------|
| `performance-optimizer.md` | → `system-optimization-engineer.md` |
| `product-manager.md` | → `product-planning-manager.md` |
| `qa-engineer.md` | → `quality-assurance-engineer.md` |
| `ai-integration-specialist.md` | → `ai-integration-expert.md` |
| `code-bug-analyzer.md` | 공식 세트 외, QA 역할과 중복 |
| `code-reviewer.md` | 공식 세트 외, QA 역할과 중복 |

### 5.2 정리 후 `.cursor/agents/` (최종)

```
.cursor/agents/
├── system-optimization-engineer.md
├── ux-design-advisor.md
├── product-planning-manager.md
├── backend-developer.md
├── frontend-developer.md
├── quality-assurance-engineer.md
├── ai-integration-expert.md
└── backup-report-github-manager.md
```

---

## STEP 6 — Rules · Agent · Report 관계

| 계층 | 경로 | 역할 |
|------|------|------|
| 전역 YAML | `.cursorrules` | 프로젝트 요약·8섹션 |
| Cursor Rules | `.cursor/rules/magicsquare-*.mdc` (5파일) | alwaysApply / glob별 규칙 |
| Cursor Agents | `.cursor/agents/*.md` (8파일) | **역할별 협업 페르소나·워크플로** |
| 설계 SSOT | `Report/02-tdd-design-report.md` | 계약·invariant·TC-ID |

**Agent는 Rules를 대체하지 않는다.** Agent는 “누가 무엇을 어떤 순서로 하는지”를 정의하고, Rules·Report/02가 “무엇이 금지·필수인지”를 정의한다.

---

## 미해결 항목 (변경 없음)

- [ ] Report/02 ↔ `.cursorrules` ECB harmonization
- [ ] DT-01 (`MagicSquareJudge`) Red 테스트부터 마방진 핵심 구현
- [ ] boundary / control / data 레이어 구현
- [ ] `pytest-cov` CI 및 커버리지 gate
- [ ] README에 Agent 8종 목록 반영 (선택)

---

## 다음 단계 (권장 순서)

1. Cursor **Agent picker**에서 8 Agent 인식 확인
2. `backend-developer` + `product-planning-manager`로 DT-01 Red 테스트 착수
3. `quality-assurance-engineer`로 TC-ID·계약 회귀 체크리스트 운영
4. (선택) `README.md`에 `.cursor/agents/` 섹션 추가

---

## 부록 A — 생성·삭제·갱신 파일 (본 세션 전체)

| 동작 | 경로 |
|------|------|
| 생성·갱신 | `.cursor/agents/` 8파일 (§STEP 4) |
| 삭제 | `.cursor/agents/` 레거시 6파일 (§STEP 5) |
| 생성 | `Report/05-cursor-agents-prompt-set-report.md` |
| 생성 | `Prompting/05-cursor-agents-prompt-set-prompt.md` |

---

## 부록 B — 관련 프롬프팅

| 문서 | 설명 |
|------|------|
| `Prompting/05-cursor-agents-prompt-set-prompt.md` | 본 단계 Cursor 대화 Transcript Export |
| `Report/04-magicsquare-rules-consolidation-report.md` | magicsquare-*.mdc 5파일 통합 |
| `Report/02-tdd-design-report.md` | 계약·invariant·TC-ID SSOT |

**세션 참조:** [Cursor Agent 8종 프롬프트](e8a07210-c957-4bd1-bc6f-e4d46005e703)
