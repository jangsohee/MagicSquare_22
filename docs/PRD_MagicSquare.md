# PRD — Magic Square 4x4 TDD Practice

| Field | Value |
|---|---|
| **Document ID** | PRD-MSQ-4X4-001 |
| **Version** | 1.0 (Draft) |
| **Status** | Pre-implementation baseline |
| **Primary SSOT (Contract & TC-ID)** | `Report/02-tdd-design-report.md` |
| **Primary SSOT (Epic / Story / AC)** | `Report/06-user-journey-to-scenario-verification-report.md` |
| **Target save path** | `docs/PRD_MagicSquare.md` |

---

## 1. Executive Summary

Magic Square 4×4 TDD Practice는 **알고리즘 난이도가 아니라** 불변식 기반 설계·검증 사고, **입력/출력 계약 고정**, **Boundary와 Domain 분리**, **Dual-Track UI + Logic TDD**, **RED → GREEN → REFACTOR** 흐름을 훈련하기 위한 구현 전 기준 문서이다. 부분적으로 채워진 4×4 격자(`0` = 빈칸, 정확히 2개)에 대해 Boundary가 입력을 검증한 뒤, Domain이 누락 숫자 2개를 두 가지 배치 순서로 시도하여 **마방진 완성 가능 시** `int[6]` = `[r1,c1,n1,r2,c2,n2]`(1-index)를 **결정론적으로** 반환한다. 완성 불가 시 정의된 오류 응답을 반환하며, 입력 검증 실패 시 Domain resolver는 **0회** 호출된다. 본 PRD의 모든 요구사항은 테스트 가능한 문장으로 작성되었으며, Concept → Rule → Use Case → Contract → Test → Component 추적성을 §21에서 보장한다.

---

## 2. Background

4×4 마방진은 규모가 작고(1~16), 규칙이 명확하며(행·열·대각 합 동일), 맞음/틀림을 자동 검증하기에 적합한 **교육·훈련 도메인**이다. 그러나 표면 목표인 “마방진 프로그램을 만든다”는 **해결책을 문제 정의에 포함**하며, 사용자 불편·성공 기준·학습 목표를 담지 못한다.

실제로 다루는 문제는 다음과 같다.

> 4×4 격자에 숫자를 배치할 때, **‘완성’이 무엇인지**·**‘지금 상태가 규칙을 어기는지’**를 사람이 반복 계산하지 않고도 **즉시·일관되게** 알 수 있어야 한다. 학습자는 그 판단 기준을 먼저 고정하고, 작은 단위로 검증 가능한 형태로 쌓으며, AI 도구와 **검증 가능한 진술**을 공유하는 최소 피드백 루프를 경험한다.

본 프로젝트는 **단순 퍼즐 풀이 앱이 아니라**, 규칙·계약·테스트·리팩토링을 통해 **신뢰할 수 있는 상태 판단**을 만드는 TDD 훈련 프로젝트이다. 실행 환경은 **콘솔·pytest 중심**이며, UI 화면·DB·Web 서버는 범위 밖이다.

---

## 3. Problem Statement

### 3.1 Problem (not solution)

| Anti-goal (금지) | Correct framing |
|---|---|
| “4×4 마방진을 자동으로 만들고 검증하는 프로그램을 만든다.” | **검증 가능한 불변식 조건**을 만족하는지 판단하고, 부분 격자에 대해 **계약된 출력** `int[6]`을 반환한다. |

### 3.2 Core problem

학습자·호출자는 다음 불편을 겪는다.

- **수동 검증 피로**: 16칸 이후 행·열·대각 합 반복 계산, 실수 발생.
- **늦고 거친 피드백**: “틀렸다”만 알고 어느 제약이 깨졌는지 역추적 필요.
- **구현 우선·테스트 기준 불명**: 구현이 먼저 시작되고, pass/fail 기준이 drift.
- **Boundary·Domain 혼합**: 입력 검증과 마방진 판정이 한 레이어에 섞임.
- **리팩토링 후 계약 파손**: `int[6]` 포맷·Error message·1-index 규칙이 깨짐.

### 3.3 Why I/O contract is central

동일한 격자 상태에 대해 **항상 동일한** 성공/실패·`int[6]`·Error code가 나와야 Red 테스트가 의미를 갖는다. 입출력 계약이 고정되지 않으면 Given/When/Then·TC-ID·Traceability를 작성할 수 없다.

---

## 4. Why Now / Why Chain

| Why level | Question | Answer (testable claim) |
|---|---|---|
| **Why #1** | 왜 마방진인가? | 4×4·1~16·합=34 규칙이 **명시 가능**하고 자동 검증에 적합하다. |
| **Why #2** | 왜 프로그램인가? | 동일 규칙을 **재현 가능**하게 적용하고, 부분 상태에서 pass/fail을 **즉시** 반환한다. |
| **Why #3** | 왜 TDD·Dual-Track인가? | 완성 정의·부분 상태 의미·판정 일관성을 **테스트로 먼저 고정**하고, Boundary 계약(Track A)과 Domain 불변식(Track B)을 **병렬**로 쌓는다. |
| **Why now** | 왜 지금인가? | 설계 보고서(Report/02)·User Journey(Report/06)가 고정되었고, **구현 전 PRD**로 계약 drift를 막아야 한다. |

---

## 5. Target Users

| User | Need | Environment |
|---|---|---|
| **TDD 학습자** | Red → Green → Refactor로 한 TC-ID씩 진행 | 로컬 Python 3.10+, pytest |
| **코드 리뷰어** | 레이어 경계·계약·Traceability 검증 | PR diff, Report/02 TC-ID |
| **Clean Architecture / ECB 학습자** | boundary → control → entity 의존 방향 훈련 | `src/magicsquare/{boundary,control,entity}/` |
| **Out of primary scope** | 최종 퍼즐 사용자(학생·교사) | 본 PRD 1차 Persona는 **개발 학습자** |

**사용 환경:** CLI/API 진입점은 Boundary 계약을 노출할 수 있으나, **그래픽 UI·DB·Web·네트워크**는 Out-of-Scope이다.

---

## 6. Vision & Epic Goal

### 6.1 Vision

**불변식 기반 사고 훈련 시스템**: 부분 4×4 격자에 대해 마방진 완성 가능 여부와 유효한 `[r1,c1,n1,r2,c2,n2]`를 **규칙·계약·테스트로 일관 제공**한다.

### 6.2 Epic Goal

| Goal type | Statement | Verification |
|---|---|---|
| **Business** | 유효 입력에 대해 계약된 `int[6]` 또는 정의된 Error를 반환한다. | IT-OK-01, UT-09, DT-05 |
| **Learning** | Concept → Invariant → Contract → Test 추적; Dual-Track TDD; Refactor 후 **외부 입출력 계약 불변** | §21 Matrix, REG-01~06 (Report/02) |
| **Quality** | Domain Logic coverage ≥ **95%**; Boundary 입력 계약 경로 **100%** UT-01~08 커버 | §14, §16 |

---

## 7. Persona

**이름:** TDD·Clean Architecture 학습 중인 개발자

**목표:** 알고리즘 “정답”보다 **설계·계약·테스트·리팩토링** 흐름을 익힌다.

**행동:** Report/02 TC-ID에 맞춰 Red 테스트를 먼저 작성하고, pytest FAIL을 확인한 뒤 최소 Green을 구현한다.

**성공 기준:** 동일 Given 격자에 대해 항상 동일 Then; Boundary 실패 시 Domain Mock 호출 **0회**.

---

## 8. User Journey Summary

| Stage | Pain Point | Learning Outcome |
|---|---|---|
| **1. Problem Recognition** | “앱 만든다”로 범위가 흐려짐 | INV-G*, INV-D*를 설계 기준으로 인식 |
| **2. Contract Definition** | 테스트 기준 불명 | 입출력·Error·Given/Then을 먼저 고정 |
| **3. Domain Separation** | 검증·판정·메시지 혼합 | Blank/Missing/Judge/Solver 책임 분리, ECB |
| **4. Dual-Track TDD** | 한 트랙만 구현 후 통합 실패 | UT-xx ∥ DT-xx Red→Green→Refactor, Mock 정책 |
| **5. Regression Protection** | 리팩토링 후 계약 깨짐 | IT-OK/FAIL, Error message 바이트 동일, `int[6]` 불변 |

---

## 9. Scope

### 9.1 In-Scope

- FR-01 ~ FR-05 (§10)
- Boundary 입력 검증 및 Error 응답 (Track A)
- Domain 빈칸·누락·판정·두 조합 Solver (Track B)
- Control/Application 오케스트레이션 (Boundary → Domain → Response)
- 선택: Data Layer 격자/결과 save·load (Report/02 §3; MVP는 **선택** — §22 참고)
- RED-GREEN-REFACTOR, pytest, AAA, Traceability Matrix

### 9.2 Out-of-Scope

- UI 화면 개발 (그래픽)
- DB/ORM, Web/API 서버, 네트워크 오류 처리
- N×N 일반화
- 완전한 마방진 **생성** 알고리즘 (빈 격자부터 생성)
- 사용자 인증/권한
- QR 스캔, 외부 서비스 연동
- Report/02·본 PRD에 없는 기능 추가

---

## 10. Functional Requirements

### FR-01 Input Verification (Boundary)

- **Description:** 호출자가 전달한 `4×4` 정수 행렬을 Domain 진입 **전**에 검증한다.
- **Layer:** Boundary
- **Input:** `grid: int[4][4]` (non-null when reachable)
- **Processing Rules:**
  1. 검증 순서는 **고정**: `NULL → ROWS → COLS → RANGE → EMPTY_COUNT → DUPLICATE`
  2. **첫 번째** 위반 1건만 반환한다.
  3. 위반 시 Domain resolver(`solve_partial_grid` 등) **호출 0회**
- **Output:** `status="ERROR"`, `code`, `message` (§13 표와 **완전 일치**)
- **Acceptance Criteria:**
  - AC-FR01-01: `grid is null` → `ERR_NULL_GRID`, Domain 0회 (UT-01)
  - AC-FR01-02: 행 수 ≠ 4 → `ERR_GRID_ROWS`, Domain 0회 (UT-02)
  - AC-FR01-03: 열 수 ≠ 4 → `ERR_GRID_COLS`, Domain 0회 (UT-03)
  - AC-FR01-04: 셀 ∉ `{0}∪[1,16]` → `ERR_VALUE_RANGE` (UT-04, UT-05, SC-BND-VAL-003)
  - AC-FR01-05: `count(0) ≠ 2` → `ERR_EMPTY_COUNT` (UT-06, UT-07, SC-BND-VAL-001)
  - AC-FR01-06: non-zero 중복 → `ERR_DUPLICATE`, message `Duplicate non-zero value: {value}.` (UT-08, SC-BND-VAL-002)
  - AC-FR01-07: 검증 통과 시 Domain **정확히 1회** 호출 (UT-09 전제)
- **Error / Exception Policy:** §13 Boundary Error 표
- **Related Business Rules:** BR-01, BR-02, BR-03, BR-04
- **Related Test Direction:** Track A — UT-01 ~ UT-08
- **Component Candidate:** `BoundaryValidator`, `ErrorFactory`, `ResponseMapper`

---

### FR-02 Blank Coordinate Discovery (Domain)

- **Description:** row-major(행 우선, 행↑ 열↑) 스캔으로 빈칸 `0` 좌표 2개를 반환한다.
- **Layer:** Control (오케스트레이션) + Domain logic (`EmptyCellScanner` 후보)
- **Input:** UI/Boundary 검증 통과 `Grid4x4` (INV-G1~G4 만족)
- **Processing Rules:**
  1. `(r1,c1)` = 첫 `0`, `(r2,c2)` = 두 번째 `0`
  2. 좌표는 **1-index**, `1 ≤ r*,c* ≤ 4`
  3. 빈칸 ≠ 2이면 `INVALID_STATE` (Boundary에서 차단되지 않은 우회 입력)
- **Output:** `(CellCoordinate, CellCoordinate)` 또는 `INVALID_STATE`
- **Acceptance Criteria:**
  - AC-FR02-01: UT-09/DT-03 격자 → `(3,3)`, `(4,4)` (DT-03)
  - AC-FR02-02: FIX-MAGIC에서 (1,1)=0,(4,4)=0 → `(1,1)`, `(4,4)` (DT-06 전제)
  - AC-FR02-03: 빈칸 3개 → `INVALID_STATE` (DT-08)
- **Error / Exception Policy:** `DomainError.INVALID_STATE`
- **Related Business Rules:** BR-05, BR-11
- **Related Test Direction:** Track B — DT-03, DT-07, DT-08
- **Component Candidate:** `BlankFinder` / `EmptyCellScanner`

---

### FR-03 Missing Number Discovery (Domain)

- **Description:** 격자에 없는 숫자 2개를 `{1..16} \ present`로 계산한다.
- **Layer:** Control + Domain (`MissingNumberResolver`)
- **Input:** 검증 통과 `Grid4x4`
- **Processing Rules:**
  1. `0`은 present 집합에서 제외
  2. 차집합 크기 = **2** (아니면 `INVALID_STATE`)
  3. `(small, large)` where `small < large`
- **Output:** `MissingPair(small, large)`
- **Acceptance Criteria:**
  - AC-FR03-01: DT-03 격자 → `(1, 7)` (DT-04)
  - AC-FR03-02: present 개수 ≠ 14 (차집합 ≠ 2) → `INVALID_STATE` (DT-09)
- **Error / Exception Policy:** `DomainError.INVALID_STATE`
- **Related Business Rules:** BR-06, BR-07
- **Related Test Direction:** Track B — DT-04, DT-09
- **Component Candidate:** `MissingNumberFinder` / `MissingNumberResolver`

---

### FR-04 Magic Square Validation (Domain)

- **Description:** 빈칸 없는 4×4 격자가 **10개 선**의 합이 모두 **34**인지 판정한다.
- **Layer:** Domain (`MagicSquareJudge`)
- **Input:** 빈칸 없는 `Grid4x4`
- **Processing Rules:**
  1. 검사 선: row1~4, col1~4, mainDiag, antiDiag (**10선**)
  2. `TARGET_LINE_SUM = 34`는 **단일 명명 상수**에서만 참조 (하드코딩 `34` 금지)
  3. 빈칸 존재 시 `INVALID_STATE`
- **Output:** `true` | `false`
- **Acceptance Criteria:**
  - AC-FR04-01: FIX-MAGIC → `true` (DT-01)
  - AC-FR04-02: FIX-MAGIC 한 행 합 ≠ 34 → `false` (DT-02)
  - AC-FR04-03: 빈칸 있는 격자로 `isMagicSquare` 호출 → `INVALID_STATE` (DT-11)
- **Error / Exception Policy:** 빈칸 있음 → `INVALID_STATE`; 판정 실패는 `false` (예외 아님)
- **Related Business Rules:** BR-08, BR-09
- **Related Test Direction:** Track B — DT-01, DT-02, DT-11, DT-12
- **Component Candidate:** `MagicSquareValidator` / `MagicSquareJudge`

---

### FR-05 Two-Combination Solver and Result Formatting (Domain + Boundary bridge)

- **Description:** 누락 숫자를 두 배치 순서로 시도하여 마방진이 되면 `int[6]`을 반환한다.
- **Layer:** Control (`SolutionAssigner`, `solve_partial_grid`) + Boundary (응답 매핑)
- **Input:** 검증 통과 `Grid4x4`
- **Processing Rules:**
  1. **Attempt 1 (small-first):** `small → (r1,c1)`, `large → (r2,c2)`; magic이면 `[r1,c1,small,r2,c2,large]`
  2. **Attempt 2 (reverse):** `large → (r1,c1)`, `small → (r2,c2)`; magic이면 `[r1,c1,large,r2,c2,small]`
  3. 둘 다 실패 → `DomainError.NO_COMPLETION` → Boundary `ERR_NO_SOLUTION` (§13)
  4. Boundary는 Domain `int[6]`을 **재정렬·0-index 변환 없이** `result`에 전달
- **Output:**
  - 성공: `status="OK"`, `result: int[6]`, `len(result)==6`
  - 실패: `ERR_NO_SOLUTION`
- **Acceptance Criteria:**
  - AC-FR05-01: UT-09 Given → `[3,3,1,4,4,7]` (DT-05, IT-OK-01)
  - AC-FR05-02: reverse only 성공 격자 G_SOL_REVERSE → `[3,3,6,4,4,1]` (SC-DOM-SOL-001)
  - AC-FR05-03: DT-06 입력 → `[1,1,16,4,4,1]` (forward 성공)
  - AC-FR05-04: 두 조합 모두 실패 → `ERR_NO_SOLUTION`, message 고정 (DT-10, UT-10, IT-FAIL-02)
  - AC-FR05-05: `{result[2],result[5]} == MissingPair` (집합 동일)
  - AC-FR05-06: `result[0],result[1],result[4],result[5] ∈ [1,4]` (UT-11)
- **Error / Exception Policy:** `NO_COMPLETION` → `ERR_NO_SOLUTION`; Domain `INVALID_STATE` 우회 시 `ERR_INTERNAL`
- **Related Business Rules:** BR-05~BR-11, BR-12~BR-14
- **Related Test Direction:** Track B — DT-05~07, DT-10; Track A — UT-09~11; Integration — IT-OK-01, IT-FAIL-02
- **Component Candidate:** `Solver` / `SolutionAssigner`, `ResultFormatter`

---

## 11. Business Rules / Domain Rules

| ID | Rule (always true when applicable) |
|---|---|
| **BR-01** | 격자는 **정확히 4행×4열**이다. |
| **BR-02** | `0`(빈칸)은 **정확히 2개**이다. |
| **BR-03** | 각 셀 값 ∈ `{0} ∪ {1,2,…,16}`이다. |
| **BR-04** | `0`이 아닌 값은 격자 내 **최대 1회** 등장한다 (중복 금지). |
| **BR-05** | 첫 빈칸 `(r1,c1)`은 **row-major** 스캔에서 **처음** 나온 `0`이다. |
| **BR-06** | 누락 숫자 집합 = `{1..16} \ present_non_zero}`이며 **크기 = 2**이다. |
| **BR-07** | 누락 숫자는 `(small, large)`로 표현하고 **`small < large`**이다. |
| **BR-08** | Magic Constant: 4×4·1~16 완성 격자에서 **모든 검사 선 합 = 34**이다. |
| **BR-09** | 검사 대상은 **10선**: 4행 + 4열 + 주대각 + 부대각이다. |
| **BR-10** | 출력 좌표 `(r1,c1)`, `(r2,c2)`는 **1-index**이고 `1 ≤ r,c ≤ 4`이다. |
| **BR-11** | 출력 `(r1,c1) ≠ (r2,c2)`이다. |
| **BR-12** | 출력은 **`int[6]`** = `[r1,c1,n1,r2,c2,n2]`이다. |
| **BR-13** | `{n1,n2}` = MissingPair (집합 동일)이다. |
| **BR-14** | small-first가 magic이면 `n1=small,n2=large` 순; 아니면 reverse 성공 시 `n1=large,n2=small` 순이다. |
| **BR-15** | Boundary 검증 실패 시 Domain solver **호출 횟수 = 0**이다. |
| **BR-16** | 성공 시 Boundary `result`는 Domain 출력과 **요소별 동일**하다 (재정렬 금지). |

---

## 12. Input / Output Contract

### 12.1 Input Contract

| Field / Item | Type | Rule | Valid Example | Invalid Example | Error Code |
|---|---|---|---|---|---|
| `grid` | `int[][]` | non-null | 4×4 배열 | `null` | `ERR_NULL_GRID` |
| `grid.length` | int | = 4 | 4 | 3 | `ERR_GRID_ROWS` |
| `grid[r].length` | int | 각 = 4 | 4 | 3 | `ERR_GRID_COLS` |
| `grid[r][c]` | int | ∈ `{0}∪[1,16]` | `0`, `7` | `17`, `-1` | `ERR_VALUE_RANGE` |
| `count(0)` | int | = 2 | 2 | 1, 3 | `ERR_EMPTY_COUNT` |
| non-zero set | set | size = count(non-zero) | unique | two `5`s | `ERR_DUPLICATE` |

**검증 순서:** `NULL → ROWS → COLS → RANGE → EMPTY_COUNT → DUPLICATE`

**첫 위반 1건만** 반환.

### 12.2 Output Contract — Success

| Field | Type | Rule | Valid Example | Invalid Example | Failure Policy |
|---|---|---|---|---|---|
| `status` | string | `"OK"` (대문자) | `"OK"` | `"ok"` | N/A (contract violation) |
| `result` | `int[6]` | `[r1,c1,n1,r2,c2,n2]`, 1-index, Domain 그대로 | `[3,3,1,4,4,7]` | length≠6, 0-index | Test failure |
| `result[2],result[5]` | int | MissingPair | `1`, `7` | 다른 집합 | Test failure |
| filled grid | — | 10선 합 = 34 | UT-09 solve 후 | — | `NO_COMPLETION` |

### 12.3 Output Contract — Error

| Field | Type | Rule |
|---|---|---|
| `status` | string | `"ERROR"` |
| `code` | string | §13 표 |
| `message` | string | §13 표 (**바이트 동일**, `{value}` 치환만 허용) |

### 12.4 Canonical Grids (Representative Test Data)

| ID | Purpose | Grid (4×4) | Expected |
|---|---|---|---|
| **FIX-MAGIC** | 완성 마방진 | `[16,3,2,13],[5,10,11,8],[9,6,7,12],[4,15,14,1]` | `isMagicSquare=true` |
| **G_PARTIAL_FWD** | small-first 성공 | `[16,3,2,13],[5,10,11,8],[9,6,0,12],[4,15,14,0]` | `[3,3,1,4,4,7]` |
| **G_SOL_REVERSE** | reverse only | `[16,2,3,13],[5,11,10,8],[9,7,0,12],[4,14,15,0]` | `[3,3,6,4,4,1]` |
| **G_INVALID_ROWS** | 3×4 | 3 rows | `ERR_GRID_ROWS` |
| **G_INVALID_BLANK** | zero×1 | one `0` | `ERR_EMPTY_COUNT` |
| **G_INVALID_DUP** | two `5`s | duplicate | `ERR_DUPLICATE` |
| **G_INVALID_RANGE** | cell `17` | — | `ERR_VALUE_RANGE` |

---

## 13. Error / Failure Policy

### 13.1 Boundary validation errors (Domain resolver **0회**)

| Condition | Error Code | Message (fixed) | Layer | Domain Call | AC / TC |
|---|---|---|---|---|---|
| `grid == null` | `ERR_NULL_GRID` | `Input grid is null.` | Boundary | 0 | UT-01 |
| row count ≠ 4 | `ERR_GRID_ROWS` | `Grid must have exactly 4 rows.` | Boundary | 0 | UT-02 |
| any row len ≠ 4 | `ERR_GRID_COLS` | `Each row must have exactly 4 columns.` | Boundary | 0 | UT-03 |
| cell ∉ {0}∪[1,16] | `ERR_VALUE_RANGE` | `Cell value must be 0 or between 1 and 16 inclusive.` | Boundary | 0 | UT-04, UT-05, SC-BND-VAL-003 |
| zero count ≠ 2 | `ERR_EMPTY_COUNT` | `Grid must contain exactly 2 empty cells (value 0).` | Boundary | 0 | UT-06, UT-07, SC-BND-VAL-001 |
| non-zero duplicate | `ERR_DUPLICATE` | `Duplicate non-zero value: {value}.` | Boundary | 0 | UT-08, SC-BND-VAL-002 |

`{value}` = row-major **최초** 중복 non-zero.

### 13.2 Domain solve failures (Boundary 검증 **통과 후**)

| Condition | Domain signal | Boundary response | Domain Call | AC / TC |
|---|---|---|---|---|
| 두 배치 모두 magic 아님 | `NO_COMPLETION` | `ERR_NO_SOLUTION` / `No magic square completion exists for the given grid.` | 1 (solve) | DT-10, UT-10, IT-FAIL-02 |
| Domain 전제 위반 (우회) | `INVALID_STATE` | `ERR_INTERNAL` / `Internal domain error: invalid grid state.` | 1 | UT-12 |

**확정:** 두 조합 모두 실패 시 **예외를 호출자에게 던지지 않고**, Boundary는 **`status="ERROR"`, `code="ERR_NO_SOLUTION"`** 응답 객체를 반환한다 (Report/02 §2.2, UC-D04-7).

### 13.3 Success response

| Field | Value |
|---|---|
| `status` | `"OK"` |
| `result` | `int[6]` per §12.2 |

---

## 14. Non-Functional Requirements

| ID | Requirement | Verification |
|---|---|---|
| **NFR-01** | Domain Logic line coverage ≥ **95%** | pytest-cov, Report/02 §4.4 |
| **NFR-02** | Boundary (validator + response) line coverage ≥ **85%** | UT-01~08 전 path |
| **NFR-03** | Data layer (if implemented) line coverage ≥ **80%** | ST-01~07 |
| **NFR-04** | **Deterministic:** 동일 `grid` 입력 → 동일 `result` 또는 동일 Error code/message | 반복 실행 테스트 |
| **NFR-05** | **No observable input mutation:** 시스템은 호출자가 전달한 `grid`의 셀 값을 **변경하지 않는다** (solve는 내부 복사본 사용) | 격자 동등성 before/after assert |
| **NFR-06** | **Performance:** 단일 solve 호출은 4×4 기준 **50ms 이내** (로컬 개발 머신, cold start 제외) | 단순 벤치마크 100회 p99 |
| **NFR-07** | Boundary는 Domain invariant·판정 로직을 **구현하지 않는다** | code review + layer import 규칙 |
| **NFR-08** | Magic Constant `34`는 **`MagicConstant.TARGET_LINE_SUM` 단일 출처**; literal `34` in logic 금지 | lint/review |
| **NFR-09** | Refactor 후 **외부** 입출력 계약·Error message·`int[6]` 스키마 **불변** (변경 시 Major + 전 테스트 갱신) | REG-01, REG-02 |
| **NFR-10** | Integration 테스트에서 control/entity **Mock 금지** | IT-* 실구현 |
| **NFR-11** | Boundary 테스트에서 Domain **Mock 허용** (호출 횟수·반환값만) | UT-09~11 |

---

## 15. Dual-Track TDD Strategy

### 15.1 Track A — Boundary / UI Contract TDD

| Item | Rule |
|---|---|
| **Scope** | 입력 검증, Error code/message, Success `int[6]` 포맷, Domain 미호출 |
| **Start TC** | UT-01 (null) → UT-06 → UT-08 → UT-04 (Report/06 권장 순) |
| **Mock** | Domain `solve_partial_grid` Mock **허용** |
| **RED** | TC-ID 1개, pytest **FAIL** 확인 후 Green |
| **Assert** | `message` **완전 문자열 일치**; Mock 호출 0 또는 1 |

### 15.2 Track B — Domain / Logic Invariant TDD

| Item | Rule |
|---|---|
| **Scope** | 빈칸, 누락, 10선=34, small-first/reverse, NO_COMPLETION |
| **Start TC** | DT-01 (FIX-MAGIC true) → DT-03 → DT-04 → DT-05 → SC-DOM-SOL-001 |
| **Mock** | **금지** (순수 Domain/Control) |
| **RED** | Given 격자·Then `int[6]` 리터럴 **고정** |
| **Invariant** | 각 TC는 INV-ID 1개 이상 명시 |

### 15.3 Parallel Progression Rules

1. Track A RED와 Track B RED는 **분리**한다.
2. 각 Track의 GREEN은 **해당 Red 1개만** 통과시키는 최소 구현이다.
3. REFACTOR는 **전체 Green 후**에만 수행하며 observable behavior는 변경하지 않는다.
4. **금지:** Domain 전부 완료 후 Boundary만 붙이는 순차 통합만으로 마일스톤을 닫지 않는다 — UT-01~04와 DT-01~03을 **교차 병렬** 진행한다.
5. **금지:** assert 완화, `skip`, `xfail`, Red 없이 `src/` 동작 추가.
6. 한 사이클 = **하나의 TC-ID** + 최소 Green + Refactor.

---

## 16. Test Plan / QA

### 16.1 Normal Scenarios

| ID | Scenario | Given | Then | TC |
|---|---|---|---|---|
| TP-N-01 | small-first 성공 | G_PARTIAL_FWD | OK, `[3,3,1,4,4,7]` | DT-05, IT-OK-01 |
| TP-N-02 | reverse only 성공 | G_SOL_REVERSE | OK, `[3,3,6,4,4,1]` | SC-DOM-SOL-001 |
| TP-N-03 | 완성 격자 판정 | FIX-MAGIC | `isMagicSquare=true` | DT-01 |

### 16.2 Exception Scenarios

| ID | Scenario | Then | TC |
|---|---|---|---|
| TP-E-01 | 3×4 grid | `ERR_GRID_ROWS`, Domain 0 | UT-02 |
| TP-E-02 | zero×1 | `ERR_EMPTY_COUNT`, Domain 0 | UT-06, SC-BND-VAL-001 |
| TP-E-03 | cell 17 | `ERR_VALUE_RANGE`, Domain 0 | UT-04, SC-BND-VAL-003 |
| TP-E-04 | duplicate 5 | `ERR_DUPLICATE`, Domain 0 | UT-08, SC-BND-VAL-002 |
| TP-E-05 | both assignments fail | `ERR_NO_SOLUTION` | DT-10, IT-FAIL-02 |

### 16.3 Boundary Scenarios

| ID | Check | Then |
|---|---|---|
| TP-B-01 | min value 1, max 16 in cells | valid when other rules hold |
| TP-B-02 | `0` only as empty | not counted in duplicate set |
| TP-B-03 | output coords | all in [1,4] |
| TP-B-04 | result length | exactly 6 |

### 16.4 Integration (end-to-end, no Domain Mock)

| ID | Scenario | TC |
|---|---|---|
| TP-I-01 | UT-09 grid full pipeline | IT-OK-01 |
| TP-I-02 | invalid blank count, Domain 0 calls | IT-FAIL-01 |
| TP-I-03 | DT-10 grid → NO_SOLUTION path | IT-FAIL-02 |

### 16.5 Level 5 Readiness (Report/06)

| Metric | Value |
|---|---|
| Epic→Story alignment | Pass |
| L4 Gherkin coverage | **Partial** — 4 core scenarios; remainder via Report/02 TC backlog |
| Recommended first RED | **DT-01** or **UT-04** |

---

## 17. Architecture Overview (High-Level)

### 17.1 Layers (ECB)

| Layer | Responsibility | MUST NOT |
|---|---|---|
| **Boundary** | 입력 검증, Error/Success 응답, `int[6]` passthrough | 마방진 판정, 누락 계산, result 재정렬 |
| **Control** | `solve_partial_grid` 오케스트레이션, 서비스 조합 | HTTP/CLI framework lock-in, Error message 하드코딩 |
| **Entity (Domain)** | `Grid4x4`, invariant, `MagicConstant`, `DomainError` | I/O, UI message, 파일 |
| **Data (optional)** | `save_grid` / `load_grid` / `save_result` | Domain invariant 구현 |

### 17.2 Dependency direction

```
Boundary → Control → Entity
Data implements ports; Entity/Boundary do not import Data concrete types
```

- Entity는 Boundary·Control을 **import하지 않는다**.
- Domain은 UI, DB, Web, 파일 시스템에 **의존하지 않는다**.

### 17.3 Request flow

```
Caller --int[4][4]--> BoundaryValidator
              | fail (0 Domain calls) --> ErrorResponse
              | ok --> Control.solve_partial_grid
                        | ok --> SuccessResponse(result=int[6])
                        | NO_COMPLETION --> ErrorResponse(ERR_NO_SOLUTION)
```

### 17.4 Glossary (Report/02 ↔ ECB)

| Report/02 term | PRD / ECB term |
|---|---|
| Screen / UI Boundary | **Boundary** |
| Domain / Logic | **Entity** + **Control** (orchestration) |
| Application (optional) | **Control** (`execute`) |

---

## 18. Component Candidates

| Component | Layer | Responsibility | Input | Output | Related FR | Related Test |
|---|---|---|---|---|---|---|
| **BoundaryValidator** | Boundary | §12.1 검증 순서 | `int[4][4]` | pass / Error code | FR-01 | UT-01~08 |
| **ErrorFactory** | Boundary | 고정 message 생성 | code, optional value | message string | FR-01 | UT-01~08 |
| **ResponseMapper** | Boundary | OK/ERROR envelope | Domain result or error | `status,code,message,result?` | FR-01, FR-05 | UT-09~11 |
| **SolveOrchestrator** | Control | UC-D05 flow | `Grid4x4` | `Result[int[6]]` | FR-02~05 | DT-05~07, IT-OK-01 |
| **BlankFinder** | Control/Domain | row-major 2 empties | `Grid4x4` | 2 coords | FR-02 | DT-03, DT-08 |
| **MissingNumberFinder** | Control/Domain | set difference | `Grid4x4` | `(small,large)` | FR-03 | DT-04, DT-09 |
| **MagicSquareValidator** | Domain | 10-line sum check | full `Grid4x4` | bool | FR-04 | DT-01, DT-02 |
| **Solver** | Control/Domain | try forward/reverse | partial grid | `int[6]` or `NO_COMPLETION` | FR-05 | DT-05~07, DT-10, SC-DOM-SOL-001 |
| **ResultFormatter** | Boundary | passthrough only | `int[6]` | same array | FR-05 | UT-09, UX-05 |

---

## 19. Risks & Ambiguities

| Risk | Impact | Mitigation / Decision |
|---|---|---|
| **1-index vs 0-index 혼동** | Wrong `int[6]`, IT 실패 | PRD·테스트·API 모두 1-index; Boundary 0-index 변환 **금지** (UX-06) |
| **row-major 첫 빈칸 누락** | `r1,c1` drift | BR-05 + DT-03 고정 격자 회귀 |
| **small-first vs reverse 데이터 혼동** | 잘못된 Then | G_PARTIAL_FWD vs G_SOL_REVERSE 분리 표 (§12.4) |
| **입력 행렬 변경** | Caller side effect | NFR-05: 내부 복사만 mutate |
| **두 조합 실패 정책 누락** | 미정 API | **확정:** `ERR_NO_SOLUTION` (§13.2) |
| **literal 34 하드코딩** | Contract drift | `MagicConstant.TARGET_LINE_SUM` only (NFR-08) |
| **Boundary·Domain 혼합** | UT/DT 섞임, Mock 오용 | FR-01 BR-15; Track 분리 §15 |
| **Report/02 Screen vs ECB control/entity** | 파일 배치 혼란 | §17.4 Glossary; **Decision Needed** §22 DEC-01 |
| **L4 Gherkin incomplete** | Story AC 미전환 | Canonical backlog = Report/02 TC-ID (§23) |

---

## 20. Engineering Principles

| Principle | Requirement |
|---|---|
| **Language** | Python 3.10+ |
| **Style** | PEP8, black 88, ruff |
| **Types** | 모든 public API에 type hints + Google docstring |
| **Imports** | `from __future__ import annotations`; isort 그룹 |
| **Testing** | pytest, AAA, `test_{tc_id}_{behavior}` |
| **TDD** | Red → Green → Refactor; Red 없이 `src/` 추가 금지 |
| **Coverage** | 전체 ≥80%; entity ≥95%; boundary ≥85%; data ≥80% |
| **ECB** | boundary → control → entity; integration Mock 금지 |
| **Logging** | `print()` 금지 → `logging` |
| **Exceptions** | bare `except` / `except Exception: pass` 금지 |
| **Constants** | 설명 없는 magic number `34` 금지 |
| **Tests** | skip/xfail/assert 완화로 Green 금지 |
| **Contracts** | Report/02 Error message 변경 시 UT-01~08 동시 갱신 |
| **AI collaboration** | Given/When/Then + TC-ID로 변경 요약 |
| **Git** | 사용자 요청 없이 commit/push 금지 |

---

## 21. Traceability Matrix

| Concept / Invariant | Business Rule | Feature ID | Acceptance Criteria | Test Case Candidate | Component |
|---|---|---|---|---|---|
| 4×4 입력 | BR-01 | FR-01 | AC-FR01-02,03 | UT-02, UT-03 | BoundaryValidator |
| 빈칸 2개 | BR-02 | FR-01 | AC-FR01-05 | UT-06, UT-07, SC-BND-VAL-001 | BoundaryValidator |
| 값 범위 0 또는 1~16 | BR-03 | FR-01 | AC-FR01-04 | UT-04, UT-05, SC-BND-VAL-003 | BoundaryValidator |
| 중복 금지 | BR-04 | FR-01 | AC-FR01-06 | UT-08, SC-BND-VAL-002 | BoundaryValidator |
| row-major 첫 빈칸 | BR-05 | FR-02 | AC-FR02-01 | DT-03, DT-07 | BlankFinder |
| 누락 숫자 2개 | BR-06 | FR-03 | AC-FR03-01 | DT-04 | MissingNumberFinder |
| 누락 오름차순 | BR-07 | FR-03 | AC-FR03-01 | DT-04 | MissingNumberFinder |
| 마방진 상수 34 | BR-08 | FR-04 | AC-FR04-01 | DT-01 | MagicSquareValidator |
| 행/열/대각 10선 합 | BR-09 | FR-04 | AC-FR04-01,02 | DT-01, DT-02, DT-12 | MagicSquareValidator |
| small-first 시도 | BR-14 | FR-05 | AC-FR05-01 | DT-05, IT-OK-01 | Solver |
| reverse 시도 | BR-14 | FR-05 | AC-FR05-02 | SC-DOM-SOL-001, DT-06 | Solver |
| int[6] 반환 | BR-12 | FR-05 | AC-FR05-01~03 | UT-09, IT-OK-01 | Solver, ResponseMapper |
| 1-index 좌표 | BR-10, BR-11 | FR-02, FR-05 | AC-FR05-06 | UT-11, DT-05 | BlankFinder, ResponseMapper |
| Domain 0-call on invalid input | BR-15 | FR-01 | AC-FR01-01~06 | UT-01~08, IT-FAIL-01 | BoundaryValidator |
| NO_COMPLETION policy | BR-14 + §13 | FR-05 | AC-FR05-04 | DT-10, UT-10, IT-FAIL-02 | Solver, ErrorFactory |
| Error message frozen | — | FR-01 | AC-FR01-* | UT-01~08 | ErrorFactory |
| Result no reorder | BR-16 | FR-05 | AC-FR05-06 | UT-09, UX-05 | ResponseMapper |
| Determinism | NFR-04 | All FR | — | repeat run | All |
| No input mutation | NFR-05 | All FR | — | before/after grid | SolveOrchestrator |

---

## 22. Open Questions / Decision Needed

| ID | Topic | Conflict | Options | PRD impact until resolved |
|---|---|---|---|---|
| **DEC-01** | Magic square **core logic file placement** | Report/02: Domain Services (`MagicSquareJudge` in Domain); ECB mdc: control orchestrates, entity holds types/constants | A) Judge in entity B) Judge in control package | Component paths in §18; do not mix validation into entity |
| **DEC-02** | **Application UseCase** layer | Report/02 §4.1: optional `SolveMagicSquareUseCase` | A) Boundary→Control direct B) Thin UseCase | §17 flow diagram variant |
| **DEC-03** | **Data layer in MVP** | Report/02 includes ST-* / IT-OK-02 | A) MVP without persistence B) InMemory only | FR scope; IT-OK-02 in MVP or Phase 2 |
| **DEC-04** | **Primary end-user persona** | Report/01: Mom Test 미완, 1차 사용자 미확정 | Keep “TDD learner” vs add puzzle solver | §5, §7 marketing only |
| **DEC-05** | **RED alias IDs** (RED-BND-VAL-001) | Report/06 dual naming | Canonical = UT/DT/ST/IT only | §23 backlog naming |
| **DEC-06** | **User Entity** (Report/03) | Implemented for session/display; not in core FR | Include in PRD Phase 2 appendix only | Out of §10 FR unless DEC-03 ties session id |

**Resolved in this PRD (not open):** 두 조합 모두 실패 → `ERR_NO_SOLUTION` 응답 (not uncaught exception).

---

## 23. Appendix

### 23.1 Reference documents

| Request name | Workspace path |
|---|---|
| Report/1 Problem Definition | `Report/01-problem-definition-report.md` |
| Report/2 Design / Contract | `Report/02-tdd-design-report.md` |
| Report/3 Dev Environment | `Report/03-cursor-rules-and-implementation-report.md` |
| Report/4 User Journey | `Report/06-user-journey-to-scenario-verification-report.md` |
| Rules consolidation | `Report/04-magicsquare-rules-consolidation-report.md` |
| Cursor rules | `.cursorrules`, `.cursor/rules/magicsquare-*.mdc` |

### 23.2 Cursor Rules summary

| File | alwaysApply | Focus |
|---|---|---|
| `magicsquare-project.mdc` | yes | I/O, Red-first, Report/02 SSOT |
| `magicsquare-forbidden.mdc` | yes | 12 MUST NOT patterns |
| `magicsquare-ecb-architecture.mdc` | src/** | Layer MUST/MUST NOT |
| `magicsquare-python-code-style.mdc` | **/*.py | PEP8, hints, docstring |
| `magicsquare-tdd-testing.mdc` | tests/** | Dual-Track, coverage, IT mock policy |

### 23.3 Gherkin scenario summary (core L4)

```gherkin
Feature: Boundary input validation
  Scenario SC-BND-VAL-001 empty count not 2
    When grid has exactly one 0
    Then status is ERROR and code is ERR_EMPTY_COUNT
    And domain solver is not invoked

  Scenario SC-BND-VAL-002 duplicate non-zero
    When grid contains duplicate 5
    Then code is ERR_DUPLICATE
    And message is "Duplicate non-zero value: 5."

  Scenario SC-BND-VAL-003 value out of range
    When any cell is 17
    Then code is ERR_VALUE_RANGE

Feature: Domain solver reverse path
  Scenario SC-DOM-SOL-001 reverse assignment succeeds
    Given grid G_SOL_REVERSE
    When solve is requested
    Then result is [3, 3, 6, 4, 4, 1]
```

**Backlog (Report/02 canonical, not yet L4):** UT-01~03, DT-05 forward (G_PARTIAL_FWD), DT-10 NO_COMPLETION, IT-OK-01.

### 23.4 RED test ID candidates (canonical)

| Track | Recommended RED order |
|---|---|
| **A (Boundary)** | UT-04 → UT-06 → UT-08 → UT-01 |
| **B (Domain)** | DT-01 → DT-03 → DT-04 → DT-05 → SC-DOM-SOL-001 |
| **Integration** | IT-OK-01 (after UT-09 path + DT-05 green) |

### 23.5 Definition of Done (MVP)

- [ ] UT-01 through UT-08 pass with exact messages
- [ ] DT-01, DT-03, DT-04, DT-05 pass
- [ ] SC-DOM-SOL-001 / G_SOL_REVERSE pass
- [ ] DT-10 → ERR_NO_SOLUTION path pass
- [ ] IT-OK-01 pass without Domain Mock
- [ ] §21 Traceability rows have at least one green test each
- [ ] Coverage ≥ NFR-01, NFR-02 thresholds

---

*End of PRD — `docs/PRD_MagicSquare.md`*
