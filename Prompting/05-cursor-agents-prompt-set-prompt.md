# Magic Square — Cursor Agent 8종 프롬프트 세트 (transcript)
_Exported on 2026-05-28 from Cursor — Agent 프롬프트 설계·생성·정리 단계 대화 기록_  
_선행: `Prompting/04-magicsquare-rules-consolidation-prompt.md` · `Report/04`_  
_보고서: `Report/05-cursor-agents-prompt-set-report.md`_

---

**User**

아래 역할별 Cursor Agent 프롬프트를 작성해 주세요.

목표: MagicSquare 4x4 TDD 연습 프로젝트에서 사용할 Agent 프롬프트 세트를 만든다.

저장 위치 규칙:
- 모든 Agent 프롬프트는 `.cursor/agents/` 폴더에 저장
- Agent별 하나의 Markdown, 파일명 = Agent 이름
- 각 Agent 출력 앞에 저장 경로 명시
- **지금은 파일 생성하지 말고** 복사 가능한 텍스트만 출력

생성할 Agent (8종):
1. system-optimization-engineer
2. ux-design-advisor
3. product-planning-manager
4. backend-developer
5. frontend-developer
6. quality-assurance-engineer
7. ai-integration-expert
8. backup-report-github-manager

각 Agent 형식: 저장 경로 · Agent Name · Role · Responsibilities · Workflow · Must Not · Output Format

공통: ECB, Dual-Track TDD, Red-Green-Refactor, Report/02 계약, 공통 안전 규칙, MagicSquare I/O(4×4, int[6], magic 34, 1-index) 준수.

중요: 지금 애플리케이션 코드·테스트·파일 생성하지 않음. Agent 프롬프트 텍스트만.

---

**Cursor**

`.cursorrules`, `Report/02`, 기존 `.cursor/agents/` 초안(backend, ux, qa, performance-optimizer 등) 확인.

**8개 Agent 프롬프트**를 YAML frontmatter + 7섹션 형식으로 출력:
- system-optimization-engineer (readonly: false)
- ux-design-advisor (false)
- product-planning-manager (**readonly: true**)
- backend-developer (false)
- frontend-developer (false)
- quality-assurance-engineer (**readonly: true**)
- ai-integration-expert (false)
- backup-report-github-manager (false)

각 블록에 MagicSquare 도메인·Dual-Track·ECB·Report/02 §2.2 Error message 고정·공통 Must Not 반영.

**협업 매트릭스** 표 제공. 파일 생성은 사용자 요청 시 진행 가능하다고 안내.

---

**User**

각 블록을 해당 `.cursor/agents/<agent-name>.md` 파일로 작성해줘

---

**Cursor**

이전에 출력한 8개 프롬프트를 `.cursor/agents/`에 **Write**로 저장.

| 파일 | readonly |
|------|----------|
| system-optimization-engineer.md | false |
| ux-design-advisor.md | false |
| product-planning-manager.md | true |
| backend-developer.md | false |
| frontend-developer.md | false |
| quality-assurance-engineer.md | true |
| ai-integration-expert.md | false |
| backup-report-github-manager.md | false |

`ux-design-advisor`, `backend-developer`, `frontend-developer`는 갱신; 나머지 5개는 신규 생성.

레거시 Agent(`performance-optimizer`, `product-manager`, `qa-engineer` 등)가 아직 남아 있음 — 정리 필요 시 요청 가능하다고 안내.

---

**User**

정리해줘

---

**Cursor**

`.cursor/agents/` 및 프로젝트 내 레거시 Agent 참조 검색.

**삭제 (6개):**

| 삭제 | 대체 |
|------|------|
| performance-optimizer.md | system-optimization-engineer.md |
| product-manager.md | product-planning-manager.md |
| qa-engineer.md | quality-assurance-engineer.md |
| ai-integration-specialist.md | ai-integration-expert.md |
| code-bug-analyzer.md | (QA와 중복) |
| code-reviewer.md | (QA와 중복) |

**최종 8파일만 유지** 확인.

---

**User**

Report 폴더에 보고서 생성하고, Prompting 폴더에 Transcript도 Export 해줘

---

**Cursor**

`Report/05-cursor-agents-prompt-set-report.md` · `Prompting/05-cursor-agents-prompt-set-prompt.md` (본 문서) 생성.

---

## 세션 요약

| Turn | 사용자 요청 | 결과 |
|------|-------------|------|
| 1 | Agent 8종 프롬프트 (텍스트만) | 8블록 출력 + 협업 매트릭스 |
| 2 | `.cursor/agents/` 파일 작성 | 8파일 생성·갱신 |
| 3 | 레거시 정리 | 6파일 삭제, 공식 8개만 유지 |
| 4 | Report + Transcript Export | Report/05, Prompting/05 |

---

## 재사용 가이드

### Turn 1 — Agent 프롬프트 설계 (텍스트만)

```
MagicSquare TDD·ECB·Report/02에 맞는 Cursor Agent 8종 프롬프트 작성.
.cursor/agents/<name>.md 형식, Role/Workflow/Must Not/Output Format.
지금은 파일 생성하지 말고 복사 가능 텍스트만.
```

### Turn 2 — 파일 생성

```
각 블록을 .cursor/agents/<agent-name>.md 로 저장
```

### Turn 3 — 레거시 정리

```
.cursor/agents/ 에서 공식 8개 외 중복·구세대 Agent 삭제
```

### Turn 4 — 문서 Export

```
Report/05 보고서 + Prompting/05 transcript Export
(Report/03·04, Prompting/03·04 형식 따름)
```

---

## 관련 산출물

| 문서 | 경로 |
|------|------|
| Agent 세트 보고서 | `Report/05-cursor-agents-prompt-set-report.md` |
| 본 Transcript | `Prompting/05-cursor-agents-prompt-set-prompt.md` |
| 공식 Agent (8) | `.cursor/agents/*.md` |
| 계약 SSOT | `Report/02-tdd-design-report.md` |
| Cursor Rules | `.cursor/rules/magicsquare-*.mdc` |

**Transcript ID:** `e8a07210-c957-4bd1-bc6f-e4d46005e703`
