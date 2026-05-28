# Magic Square — User Journey → Scenario Verification (transcript)
_Exported on 2026-05-28 from Cursor — Epic → Journey → Story → Scenario → Verification (Level 1~5) 대화 기록_  
_선행: `Report/02-tdd-design-report.md`, `Report/05-cursor-agents-prompt-set-report.md`_

---

**User**

Magic Square 프로젝트의 User Journey를 다음 구조로 만들고 싶습니다.

Epic → User Story → Task

지금은 Level 1: Epic, 즉 Business Goal만 작성합니다.

중요:
- 구현 코드를 작성하지 마십시오.
- 테스트 코드를 작성하지 마십시오.
- 파일을 생성하지 마십시오.
- 아직 User Story나 Task로 세분화하지 마십시오.
- 오직 Epic 수준의 비즈니스 목표와 학습 목표만 정의하십시오.

Epic: “불변식 기반 사고 훈련 시스템 구축”

(성공 기준: Domain 95%+, Boundary 100%, 매직 넘버 금지, Invariant 추적, Refactor 후 계약 불변 등)

출력 형식: Level 1 Epic — Business Goal (11개 섹션)

---

**Cursor**

`README.md`, `Report/02-tdd-design-report.md`, `.cursorrules`를 참조하여 **Level 1 Epic** 문서를 작성 (파일 생성 없음).

**산출 요약:**

1. **Epic Title** — 불변식 기반 사고 훈련 시스템 구축  
2. **Business Goal** — 규칙 기반 상태 판단·`int[6]` 계약 제공 (정답 생성기 아님)  
3. **Learning Goal** — Invariant·Dual-Track TDD·Concept→Test 추적·AI 협업  
4. **Problem Statement** — 표면 vs 진짜 문제; 고정 I/O Contract 표  
5. **Target Learners** — 주니어 학습자, Boundary 호출자, Cursor AI  
6. **Scope** — Domain, Boundary, Data, Integration, Dual-Track, ECB, 품질 게이트  
7. **Non-Scope** — NxN, 게임화, DB, 풀 UI, 하드코딩 Green  
8. **Success Criteria** — SC-01~17 (커버리지·계약·추적성)  
9. **Key Invariants** — INV-G1~G4, INV-D1~D7, NO_COMPLETION  
10. **Traceability Rule** — TR-01~08, Report/02 단일 진실 원천  
11. **Candidate User Stories for Level 2** — US-L2-01~12 (후보만)

---

**User**

Level 2: User Journey 작성 요청.

Persona: TDD·Clean Architecture 학습자  
Journey Goal: 불변식·계약·Domain/Boundary 분리·Dual-Track·회귀 보호  
5 Stage: Problem Recognition → Contract Definition → Domain Separation → Dual-Track TDD → Regression Protection

출력 형식: Persona, Journey Goal, Overview 표, Detailed Journey 5 Stage, Journey→Story Mapping, Traceability Link

(코드·테스트·파일 생성 금지)

---

**Cursor**

Level 1 Epic·Report/02와 정렬하여 **Level 2 User Journey** 작성.

**산출 요약:**

- **Persona:** 준 — TDD 실습 중, AI 협업 시 TC-ID·계약 기준  
- **Journey Overview:** 5 Stage × Action / Thinking / Pain / Opportunity / Outcome  
- **Stage 1:** 표면 vs 진짜 문제, INV-G*, INV-D* 인식  
- **Stage 2:** Input/Output/Error Contract, 검증 순서, UX-01~07  
- **Stage 3:** BlankFinder / MissingNumberFinder / MagicSquareValidator / Solver + ECB 배치  
- **Stage 4:** UI RED(UT-xx) ∥ Logic RED(DT-xx), GREEN 최소·REFACTOR 불변  
- **Stage 5:** IT-OK/FAIL, REG-01~06, Edge/Input/Combination/Format 회귀  
- **Journey→Story Mapping:** US-L2-01~12 후보  
- **Traceability Link:** Epic Goal ↔ Stage ↔ Invariant ↔ Test Target

---

**User**

Level 3: User Stories 작성 요청.

Story 1~5 초안 제공:
- Story 1 입력 검증 (Boundary)
- Story 2 빈칸 좌표 (Domain)
- Story 3 누락 숫자 (Domain)
- Story 4 마방진 검증 (Domain)
- Story 5 두 조합 시도 (Domain/Solver)

출력: Story Overview, Story 1~5 (Layer, AC, Protected Contract/Invariant, Future RED Direction), Traceability Matrix

(코드·테스트·파일·Task 분해 금지)

---

**Cursor**

Report/02 Error Code·TC-ID·Invariant와 정렬하여 **Level 3 User Stories** 작성.

**산출 요약:**

| Story ID | Layer | Protected |
|----------|-------|-----------|
| US-B01 | Boundary | INV-G1~G4, Error Contract |
| US-D01 | Domain | INV-D2 |
| US-D02 | Domain | INV-D1 |
| US-D03 | Domain | INV-D3, MagicConstant |
| US-D04 | Domain | INV-D5~D7, NO_COMPLETION |

- **US-B01:** AC 9건 — null/rows/cols/range/empty/dup, 첫 위반 1건, Domain 0회/1회, message 완전 일치  
- **US-D01:** AC 8건 — row-major, DT-03/07 Given, 1-index, INVALID_STATE  
- **US-D02:** AC 6건 — `{1..16}\present`, (small,large), DT-04 (1,7)  
- **US-D03:** AC 7건 — 10선=34, FIX-MAGIC, TARGET_LINE_SUM 상수  
- **US-D04:** AC 11건 — forward/reverse, DT-05/06/07, NO_COMPLETION, 하드코딩 금지  
- **Traceability Matrix:** Epic Goal ↔ Story ↔ AC ↔ UT/DT/IT

---

**User**

Level 4: Implementation Scenario — Technical

Feature: 4x4 마방jin 완성

시나리오 4건 제공:
- **SC-DOM-SOL-001** — small-first 실패, reverse 성공, `[3,3,6,4,4,1]`
- **SC-BND-VAL-001** — 빈칸 1개
- **SC-BND-VAL-002** — 중복 숫자
- **SC-BND-VAL-003** — 값 범위 (>16)

Decomposition Preview 표 포함.

---

**Cursor**

격자 수학 검증 후 **Level 4 Technical Scenarios** 정식화 (Report/02 UT-04/06/08, DT-06 패턴 매핑).

**SC-DOM-SOL-001 검증:**

```
Given:
[16,  2,  3, 13]
[ 5, 11, 10,  8]
[ 9,  7,  0, 12]
[ 4, 14, 15,  0]
```

- forward (3,3)=1, (4,4)=6 → row3=29, row4=39 → **실패**  
- reverse (3,3)=6, (4,4)=1 → 10선 합=34 → **성공**  
- **Then:** `[3, 3, 6, 4, 4, 1]` ✅

**Boundary 시나리오:**

| Scenario | Given | Then | Canonical |
|----------|-------|------|-----------|
| SC-BND-VAL-001 | zero×1 | ERR_EMPTY_COUNT, Mock 0회 | UT-06 |
| SC-BND-VAL-002 | two 5s | ERR_DUPLICATE, message exact | UT-08 |
| SC-BND-VAL-003 | cell=17 | ERR_VALUE_RANGE | UT-04 |

**RED / Task:**

- RED-DOM-SOL-001 → TASK-DOM-SOL-001 (선행 DT-05 Green 권장)  
- RED-BND-VAL-001~003 → TASK-BND-VAL-001~003  

**TDD 순서:** Boundary UT-04→06→08 ∥ Domain DT-01→03→04→05→RED-DOM-SOL-001

---

**User**

Level 5: Scenario Verification and Summary

Level 1~4 연결 검증:
- Epic→Journey→Story→Scenario
- AC 누락, Edge Case, Boundary/Domain 분리
- RED/Task 분해, Invariant 추적성

출력 형식: Overall Judgment, Consistency Checks 5종, Edge Case, Invariant, Dual-Track, Implementation, Traceability, Missing Items, Final Summary

(코드·테스트·파일 생성 금지)

---

**Cursor**

Level 1~4 및 Report/02 대조 **Level 5 Verification** 수행.

**Overall Judgment:**

| 항목 | 결과 |
|------|------|
| 적합성 | **7.5 / 10** |
| 상태 | **일부 수정 필요** |
| 판정 | Epic→Journey→Story **양호**; L4는 시드 4건; Report/02로 AC 보완; Red **조건부 가능** |

**Consistency:**

- Epic → Journey: ✅ Pass  
- Journey → Story: ⚠️ Stage 1 전용 Story 없음  
- Story → Scenario: ❌ AC 전체 Gherkin 미변환 (~30–45%)  
- Boundary/Domain: ✅ Pass  
- Dual-Track: ✅ Pass  

**Edge Case:**

- Normal reverse: ✅ SC-DOM-SOL-001  
- Normal forward: ⚠️ DT-05 only (L4 gap)  
- Exception null/rows: ⚠️ Report/02 only  
- NO_COMPLETION: ❌ L4 gap (DT-10)  

**Missing Items (필수 보강):**

1. SC-DOM-SOL-000 (forward / DT-05)  
2. SC-DOM-SOL-002 (NO_COMPLETION / DT-10)  
3. SC-BND-VAL-000 (null / UT-01)  
4. RED-* ↔ UT-xx/DT-xx canonical 매핑 확정  

**Final Summary:**

- **다음 단계:** L4 보강 후 Red 착수 **또는** Report/02 TC-ID를 official backlog로 승격  
- **권장 Red 시작점:** UT-04 (Boundary) 또는 DT-01 (Domain Judge)

---

**User**

Report 폴더에 보고서 생성하고, Prompting 폴더에 Transcript도 Export 해줘

---

**Cursor**

Level 1~5 산출물을 통합하여 다음 파일 생성:

| 파일 | 설명 |
|------|------|
| `Report/06-user-journey-to-scenario-verification-report.md` | Level 1~5 통합 보고서 + Level 5 검증 결과 |
| `Prompting/06-user-journey-to-scenario-verification-prompt.md` | 본 Transcript |

**Report/06 구성:**

- Executive Summary (적합성 7.5/10, pytest 9 passed, DT-01 미착수)  
- Level 1 Epic 요약  
- Level 2 Journey 5 Stage 요약  
- Level 3 User Stories (US-B01, US-D01~D04)  
- Level 4 Scenarios (SC-BND-VAL-001~003, SC-DOM-SOL-001)  
- Level 5 Verification (커버리지·Gap·Missing Items·Final Summary)  
- Traceability Matrix · 다음 단계 · 부록 격자  

**구현 상태:** `src/` 마방진 핵심 변경 없음 — 문서 Export만 수행

---

## 재사용 프롬프트 (Level 1~5 일괄)

```markdown
Magic Square 4×4 TDD Practice — Epic → Journey → Story → Scenario → Verification

Level 1: Epic “불변식 기반 사고 훈련 시스템 구축” (Business + Learning Goal만)
Level 2: User Journey 5 Stage (Persona: TDD 학습자)
Level 3: User Stories US-B01 + US-D01~D04 (Boundary/Domain 분리, 테스트 가능 AC)
Level 4: Gherkin Technical Scenarios + RED/Task 후보
Level 5: Level 1~4 연결 검증 + Traceability + Gap 분석

제약: 코드·테스트·파일 생성 없음 (Export 단계 제외)
단일 진실 원천: Report/02-tdd-design-report.md
고정 계약: 4×4, 0=빈칸×2, 1~16, int[6] 1-index, Magic=34, forward→reverse Solver
```

---

## 관련 문서

| 문서 | 경로 |
|------|------|
| 본 단계 보고서 | `Report/06-user-journey-to-scenario-verification-report.md` |
| TDD 설계 (TC-ID) | `Report/02-tdd-design-report.md` |
| Agent 프롬프트 세트 | `Report/05-cursor-agents-prompt-set-report.md` |
