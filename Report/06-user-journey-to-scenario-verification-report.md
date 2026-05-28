# Magic Square 프로젝트 — User Journey → Scenario Verification 보고서

**작성 목적:** Epic → User Journey → User Story → Technical Scenario → Verification (Level 1~5) 산출물을 한 흐름으로 정리하고, Level 5 검증 결과를 고정  
**대상:** 주니어 개발자 + Cursor AI 협업 학습 프로젝트  
**범위:** Level 1 Epic · Level 2 User Journey · Level 3 User Stories · Level 4 Technical Scenarios · Level 5 Verification (구현 코드·테스트 코드 제외)  
**선행 문서:** `Report/02-tdd-design-report.md`, `Report/05-cursor-agents-prompt-set-report.md`  
**작성일:** 2026-05-28

---

## Executive Summary

본 단계에서 MagicSquare 4×4 TDD Practice는 **요구사항 계층(Epic → Journey → Story → Scenario)** 을 5레벨로 분해·검증했다. 상위 3레벨(Epic·Journey·User Story)은 **불변식·계약·ECB 분리·Dual-Track TDD** 관점에서 **강하게 정렬**되었다. Level 4 Technical Scenario는 **Boundary 3건 + Domain Solver reverse 1건**을 Gherkin으로 고정했으며, `Report/02`의 UT-xx / DT-xx 카탈로그가 **나머지 Acceptance Criteria·Edge Case**를 설계 수준에서 보완한다.

| 항목 | 결과 |
|------|------|
| **Level 5 적합성 점수** | **7.5 / 10** |
| **Level 5 판정** | **일부 수정 필요** (L4 시나리오 보강 후 Red 착수 권장) |
| **Boundary / Domain 분리** | Pass |
| **Dual-Track TDD 준비** | Pass |
| **RED / Task 분해 가능** | Pass |
| **`src/` 마방진 핵심 (DT-01~)** | 미착수 (변경 없음) |

**pytest:** `9 passed` (변경 없음 — `tests/entity/test_user.py`)

**Transcript:** `Prompting/06-user-journey-to-scenario-verification-prompt.md`

---

## 문서 계층 구조

```
Level 1  Epic          “불변식 기반 사고 훈련 시스템 구축”
    ↓
Level 2  User Journey  5 Stage (인식 → 계약 → 분리 → Dual-Track → 회귀)
    ↓
Level 3  User Stories  US-B01 (Boundary) + US-D01~D04 (Domain)
    ↓
Level 4  Scenarios     SC-BND-VAL-001~003, SC-DOM-SOL-001 (+ Report/02 TC 보완)
    ↓
Level 5  Verification  연결성·AC·Edge Case·Invariant·Dual-Track 검증
```

**단일 진실 원천 (구현 착수 시):** `Report/02-tdd-design-report.md` — TC-ID · Error message · Traceability Matrix

---

# Level 1: Epic — Business Goal (요약)

## Epic Title

**불변식 기반 사고 훈련 시스템 구축** (Magic Square 4×4 TDD Practice)

## Business Goal

부분적으로 채워진 4×4 격자에 대해 **마방진 완성 가능 여부**와 **유효한 `[r1,c1,n1,r2,c2,n2]`** 를 규칙·계약·테스트로 **일관되게** 제공한다. 알고리즘 난이도가 아니라 **입출력 계약 안정성**이 핵심 성과물이다.

## Learning Goal

- 불변식 중심 설계 · Dual-Track UI + Logic TDD  
- Concept → Invariant → Contract → Test 추적성  
- Red → Green → Refactor · AI 협업(검증 가능한 진술)

## 고정 I/O Contract

| 구분 | 계약 |
|------|------|
| 입력 | `4×4 int[][]` — `0`=빈칸(2개), 값 `0` 또는 `1..16`, 0 제외 중복 금지 |
| 출력 | `int[6]` = `[r1,c1,n1,r2,c2,n2]` — **1-index** |
| 배치 | 작→첫빈·큰→둘째 magic → 그 순서, 아니면 n1,n2 반대 |
| Magic Constant | 10개 선 합 = **34** (`MagicConstant.TARGET_LINE_SUM`) |
| Boundary 검증 순서 | `NULL → ROWS → COLS → RANGE → EMPTY_COUNT → DUPLICATE` |

## Success Criteria (Epic)

- Domain Logic coverage ≥ **95%** · Boundary 입력 계약 테스트 **100%**  
- 매직 넘버·정답 하드코딩 금지 · Invariant ↔ TC 추적  
- Refactor 후 **외부 입출력 계약 불변**

---

# Level 2: User Journey (요약)

| Stage | 목적 | 핵심 Learning Outcome |
|-------|------|------------------------|
| **1. Problem Recognition** | 표면 목표 vs 진짜 문제 구분 | INV-G*, INV-D*를 설계 기준으로 인식 |
| **2. Contract Definition** | 입출력·Error 먼저 고정 | 테스트 가능한 Given/Then |
| **3. Domain Separation** | BlankFinder 등 4책임 + ECB | 레이어별 Invariant 1:1 |
| **4. Dual-Track TDD** | UT-xx ∥ DT-xx Red→Green→Refactor | Mock 정책·한 Red 한 동작 |
| **5. Regression Protection** | IT-OK/FAIL · REG 규칙 | observable behavior 불변 증명 |

**Persona:** TDD·Clean Architecture 학습 중인 개발자 — 알고리즘 정답보다 **설계·계약·테스트·리팩토링** 훈련

---

# Level 3: User Stories

## Story Overview

| Story ID | Story Name | Layer | Protected Contract / Invariant |
|----------|------------|-------|--------------------------------|
| **US-B01** | 입력 검증 | Boundary | INV-G1~G4, Error Contract, Domain 미호출 |
| **US-D01** | 빈칸 좌표 탐색 | Domain | INV-D2 |
| **US-D02** | 누락 숫자 탐색 | Domain | INV-D1 |
| **US-D03** | 마방진 검증 | Domain | INV-D3, INV-D4, MagicConstant |
| **US-D04** | 두 가지 조합 시도 | Domain | INV-D5~D7, Output Contract, NO_COMPLETION |

## US-B01 — 입력 검증 (Boundary)

**User Story:** Boundary가 Domain 호출 **전** 입력 행렬을 검증하여 invalid data가 Domain에 전달되지 않게 한다.

**Acceptance Criteria (9건):** null → ERR_NULL_GRID; rows/cols ≠ 4; RANGE; EMPTY_COUNT; DUPLICATE; 첫 위반 1건; 실패 시 Domain **0회**; 유효 입력 시 Domain **1회**.

**Report/02 매핑:** UT-01 ~ UT-08

## US-D01 — 빈칸 좌표 탐색

**Acceptance Criteria (8건):** `0` 탐지; 정확히 2좌표; row-major; FIX-MAGIC (3,3)(4,4) → (3,3),(4,4); 빈칸 3개 → INVALID_STATE; **1-index** 출력.

**Report/02 매핑:** DT-03, DT-07, DT-08

## US-D02 — 누락 숫자 탐색

**Acceptance Criteria (6건):** `0` 제외; `{1..16}\present` 크기 2; `(small,large)` 오름차순; DT-03 격자 → (1,7); present≠14 → INVALID.

**Report/02 매핑:** DT-04, DT-09

## US-D03 — 마방진 검증

**Acceptance Criteria (7건):** 10선 검사; 전부 34 → true; FIX-MAGIC true; 한 행 틀림 false; 빈칸 있으면 INVALID; `TARGET_LINE_SUM` 상수 단일 출처.

**Report/02 매핑:** DT-01, DT-02, DT-11, DT-12

## US-D04 — 두 가지 조합 시도

**Acceptance Criteria (11건):** forward → reverse; `int[6]` 1-index; DT-05 `[3,3,1,4,4,7]`; DT-06 reverse; NO_COMPLETION; Boundary 무변환; 하드코딩 금지.

**Report/02 매핑:** DT-05 ~ DT-07, DT-10, UT-10

---

# Level 4: Technical Scenarios

## Feature Background

4×4 행렬 · 0=빈칸(2개) · 1~16 · 중복 금지 · TARGET_LINE_SUM=34 · 출력 `[r1,c1,n1,r2,c2,n2]` 1-index

## Scenario Catalog

| Scenario ID | Layer | Related Story | Canonical TC-ID | RED Candidate | Task Candidate |
|-------------|-------|---------------|-----------------|---------------|----------------|
| **SC-BND-VAL-001** | Boundary | US-B01 | UT-06 | RED-BND-VAL-001 | TASK-BND-VAL-001 |
| **SC-BND-VAL-002** | Boundary | US-B01 | UT-08 | RED-BND-VAL-002 | TASK-BND-VAL-002 |
| **SC-BND-VAL-003** | Boundary | US-B01 | UT-04 | RED-BND-VAL-003 | TASK-BND-VAL-003 |
| **SC-DOM-SOL-001** | Domain/Solver | US-D04 | *(확장 — reverse)* | RED-DOM-SOL-001 | TASK-DOM-SOL-001 |

### SC-DOM-SOL-001 — reverse 성공

**Given 격자 G_SOL_REVERSE:**

```
[16,  2,  3, 13]
[ 5, 11, 10,  8]
[ 9,  7,  0, 12]
[ 4, 14, 15,  0]
```

- 빈칸: (3,3), (4,4) · 누락: (1, 6)  
- forward (1,6) → magic **실패**  
- reverse (6,1) → magic **성공**  
- **Then:** `[3, 3, 6, 4, 4, 1]`

### SC-BND-VAL-001 — 빈칸 1개

- **Then:** ERR_EMPTY_COUNT, message 고정, Domain Mock **0회**

### SC-BND-VAL-002 — 중복 5

- **Then:** ERR_DUPLICATE, `Duplicate non-zero value: 5.`, Domain **0회**

### SC-BND-VAL-003 — cell=17

- **Then:** ERR_VALUE_RANGE, message 고정, Domain **0회**

## TDD Execution Order (권장)

1. Boundary: UT-04 → UT-06 → UT-08 (L4 SC-BND-VAL-003, 001, 002)  
2. Domain: DT-01 → DT-03 → DT-04 → DT-05 → RED-DOM-SOL-001  
3. Integration: IT-OK-01 (Report/02)

---

# Level 5: Scenario Verification and Summary

## Overall Judgment

| 항목 | 값 |
|------|-----|
| 적합성 점수 | **7.5 / 10** |
| 현재 상태 | **일부 수정 필요** |
| 요약 | Epic→Journey→Story **정렬 양호**; L4는 **시드 4건** — Report/02로 AC·Edge 보완; Red 착수 **조건부 가능** |

## Story → L4 커버리지

| User Story | L4 Scenario | 커버율 | Report/02 보완 |
|------------|-------------|--------|----------------|
| US-B01 | 3 | ~33% | UT-01~03, 07, 09~11 |
| US-D01 | 0 (암시) | ~25% | DT-03, 07, 08 |
| US-D02 | 0 (암시) | ~17% | DT-04, 09 |
| US-D03 | 0 (암시) | ~29% | DT-01, 02, 11, 12 |
| US-D04 | 1 | ~45% | DT-05~07, 10, UT-10 |

## Consistency Check 요약

| 구간 | 판정 | 비고 |
|------|------|------|
| Epic → Journey | ✅ Pass | 성공 기준·Dual-Track·Pain Point 반영 |
| Journey → Story | ⚠️ Partial | Stage 1 전용 Story 없음 |
| Story → Scenario | ❌ Fail (완전 변환) | L4 4건만 Gherkin; Report/02가 보완 |
| Boundary / Domain 분리 | ✅ Pass | US-B01 vs US-D01~D04, Mock 0회 |
| Dual-Track 준비 | ✅ Pass | UT-* ∥ DT-* |
| Implementation 분해 | ✅ Pass | 4 Domain + Boundary Validator |

## Invariant Coverage (요약)

| Invariant | L4 | Status |
|-----------|-----|--------|
| INV-G2 (빈칸 2) | SC-BND-VAL-001 | ✅ |
| INV-G4 (중복) | SC-BND-VAL-002 | ✅ |
| INV-G3 (범위) | SC-BND-VAL-003 | ⚠️ (-1 미포함) |
| INV-G1 (4×4) | Report/02 only | ⚠️ |
| INV-D7 reverse | SC-DOM-SOL-001 | ✅ |
| INV-D7 forward | Report/02 DT-05 | ⚠️ |
| NO_COMPLETION | Report/02 DT-10 | ❌ L4 gap |
| int[6], 1-index | SC-DOM-SOL-001 | ✅ |

## Missing Items (반드시 보강 권장)

| 항목 | Suggested Fix |
|------|---------------|
| forward 성공 L4 없음 | **SC-DOM-SOL-000** (DT-05 → `[3,3,1,4,4,7]`) |
| NO_COMPLETION L4 없음 | **SC-DOM-SOL-002** (DT-10) |
| null/rows/cols L4 없음 | **SC-BND-VAL-000, 004, 005** (UT-01~03) |
| RED ID 이중 체계 | RED-* = 별칭, **Canonical = UT-xx / DT-xx** |
| Integration L4 없음 | **SC-INT-OK-001** (IT-OK-01) |

## Final Summary

- **검증 결과:** 상위 설계 계층은 TDD 착수 가능; L4는 핵심 경로만 Gherkin화  
- **가장 강한 부분:** 계약·Error message·Domain isolation·SC-DOM-SOL-001 수학적 검증  
- **가장 약한 부분:** Story AC → Gherkin 전환율, forward/NO_COMPLETION/Integration L4 부재  
- **다음 단계:** L4 보강 6~8건 **또는** Report/02 TC-ID를 official backlog로 승격 후 **DT-01 또는 UT-04 Red** 착수

---

## Traceability Matrix (Epic → Red)

| Epic Goal | Journey Stage | User Story | Technical Scenario | Canonical TC / RED | Task |
|-----------|---------------|------------|-------------------|-------------------|------|
| 입력 계약 | 2 | US-B01 | SC-BND-VAL-001~003 | UT-04,06,08 | TASK-BND-VAL-* |
| Solver reverse | 4,5 | US-D04 | SC-DOM-SOL-001 | RED-DOM-SOL-001 | TASK-DOM-SOL-001 |
| Solver forward | 4 | US-D04 | *(gap)* | DT-05 | TASK-DOM-SOL-000 |
| NO_COMPLETION | 5 | US-D04 | *(gap)* | DT-10 | TASK-DOM-SOL-002 |
| 불변식·판정 | 3 | US-D03 | *(gap)* | DT-01 | TASK-DOM-JUDGE-001 |
| 빈칸·누락 | 3 | US-D01,D02 | SC-DOM-SOL-001 Given | DT-03,04 | TASK-DOM-BLANK/MISS-001 |
| Integration | 5 | US-B01,D04 | *(gap)* | IT-OK-01 | TASK-INT-001 |

---

## 다음 단계 (구현 착수 전)

- [ ] L4 시나리오 보강 (§ Missing Items) 또는 Report/02 TC-ID backlog 확정  
- [ ] **DT-01** Red: `MagicSquareJudge` — FIX-MAGIC → true  
- [ ] **UT-04** Red: `ERR_VALUE_RANGE` — cell=17  
- [ ] RED ID ↔ Report/02 TC-ID 매핑표 CI/README 반영 (선택)

---

## 부록: 참고 격자

**FIX-MAGIC (Report/02):**

```
[16,  3,  2, 13]
[ 5, 10, 11,  8]
[ 9,  6,  7, 12]
[ 4, 15, 14,  1]
```

**G_SOL_REVERSE (SC-DOM-SOL-001):**

```
[16,  2,  3, 13]
[ 5, 11, 10,  8]
[ 9,  7,  0, 12]
[ 4, 14, 15,  0]
```

**기대 출력:** `[3, 3, 6, 4, 4, 1]`

---

## 변경 이력

| 날짜 | 내용 |
|------|------|
| 2026-05-28 | Level 1~5 Cursor 대화 산출물 통합 · Report/06 · Prompting/06 Export |
