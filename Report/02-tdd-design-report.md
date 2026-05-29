# Magic Square 프로젝트 — Dual-Track TDD 설계 보고서

**작성 목적:** 4×4 Magic Square — Logic / Screen(UI Boundary) / Data 레이어 분리 및 계약 기반 TDD 설계 고정  
**대상:** 주니어 개발자 + Cursor AI 활용 학습 프로젝트  
**범위:** Domain · Screen · Data · Integration 설계·계약·테스트·통합 계획 (구현 코드 제외)  
**선행 문서:** `Report/01-problem-definition-report.md`  
**작성일:** 2026-05-28

---

## Executive Summary

본 보고서는 Magic Square 4×4 프로젝트의 **Dual-Track UI + Logic TDD** 및 **Clean Architecture** 설계를 고정한다. 알고리즘 난이도보다 **레이어 분리 + 계약 기반 테스트 + 리팩토링** 훈련이 목적이다.

**고정 입출력 계약:**
- **입력:** `4×4 int[][]` — `0`=빈칸, 빈칸 정확히 2개, 값 `0` 또는 `1~16`, 0 제외 중복 금지
- **출력:** `int[6]` = `[r1,c1,n1,r2,c2,n2]` — 좌표 1-index; `n1,n2`는 누락 숫자; (작은수→첫빈칸, 큰수→둘째빈칸)이 magic이면 그 순서, 아니면 반대

**Magic Constant:** 4×4·1~16 설정에서 목표 선 합 = **34**

---

# 1) Logic Layer (Domain Layer) 설계

## 1.1 도메인 개념

| 분류 | 이름 | 책임 (SRP) | 비고 |
|------|------|------------|------|
| **Value Object** | `Grid4x4` | 4×4 정수 격자 불변 표현; 행·열 길이 4 고정 | 원시 `int[][]` 래핑 |
| **Value Object** | `CellCoordinate` | 1-index `(row, col)`; 동등성·순서 비교 | 빈칸 순서 기준 |
| **Value Object** | `MissingPair` | 누락 숫자 `(small, large)`; `small < large` 보장 | 1~16 집합 차집합 |
| **Value Object** | `MagicConstant` | 4×4·1~16 설정의 목표 합 **34** 단일 상수 | `136 / 4 = 34` |
| **Value Object** | `SolutionTuple` | `[r1,c1,n1,r2,c2,n2]` 6원소 결과 | Domain 최종 산출 |
| **Entity** | `PartialMagicGrid` | 빈칸 2개·유일성 만족 입력 격자 + 빈칸·누락 숫자 캐시 | Aggregate Root |
| **Domain Service** | `EmptyCellScanner` | row-major(행↑, 열↑) 스캔으로 빈칸 2개 좌표 반환 | 첫 빈칸=(r1,c1), 둘째=(r2,c2) |
| **Domain Service** | `MissingNumberResolver` | `{1..16} \ present` → 정확히 2개 숫자 | 개수≠2면 실패 |
| **Domain Service** | `MagicSquareJudge` | 완전 채워진 4×4가 행·열·주대각·부대각 합=34인지 판정 | boolean |
| **Domain Service** | `SolutionAssigner` | (작→첫빈칸, 큰→둘째빈칸) 시도 후 실패 시 반대 배치 | 출력 n1,n2 순서 결정 |

**Aggregate 경계:** `PartialMagicGrid`는 Domain 내부에서만 생성. UI 검증 통과 후 Domain 진입.

**Domain이 하지 않는 것:** 격자 크기·빈칸 개수·값 범위·중복 검사(UI 계약), 저장/로드(Data), 사용자 메시지 문구(Screen).

---

## 1.2 도메인 불변조건 (Invariants)

| ID | 불변조건 | 완전 격자에서의 기대 | Domain 진입 전제 |
|----|----------|----------------------|-------------------|
| **INV-G1** | 격자 크기 | 4행×4열 | UI가 보장 |
| **INV-G2** | 빈칸 개수 | `0` 값 정확히 2개 | UI가 보장 |
| **INV-G3** | 값 범위 | 각 칸 ∈ `{0} ∪ {1..16}` | UI가 보장 |
| **INV-G4** | 0 제외 유일성 | 0이 아닌 값은 격자 내 1회만 등장 | UI가 보장 |
| **INV-D1** | 누락 숫자 개수 | `{1..16} \ present` 크기 = 2 | INV-G2~G4 + MissingNumberResolver |
| **INV-D2** | 빈칸 순서 | `(r1,c1)` = row-major 첫 `0`, `(r2,c2)` = 두 번째 | EmptyCellScanner |
| **INV-D3** | Magic Constant | 완전 격자의 모든 행·열·주대각·부대각 합 = **34** | MagicSquareJudge |
| **INV-D4** | 완전성 | 판정 시 빈칸 없음 (임시 채움 후 검사) | SolutionAssigner |
| **INV-D5** | 출력 좌표 | `1 ≤ r*, c* ≤ 4` | SolutionTuple |
| **INV-D6** | 출력 숫자 | `{n1,n2} = MissingPair`, `(r1,c1)≠(r2,c2)` | SolutionAssigner |
| **INV-D7** | 배치 규칙 | 작→첫빈·큰→둘째가 magic이면 `[r1,c1,small,r2,c2,large]`, 아니면 `[r1,c1,large,r2,c2,small]` | SolutionAssigner |

**Magic Constant 정의 (고정):**

```
SUM(1..16) = 136
TARGET_LINE_SUM = 136 / 4 = 34
검사 대상 10개 선: row1..4, col1..4, mainDiag, antiDiag
```

**Domain 실패 (해결 불가):** 두 배치 모두 `MagicSquareJudge` = false → `DomainError.NO_COMPLETION`.

---

## 1.3 핵심 유스케이스 (도메인 관점)

| UC-ID | 유스케이스 | 입력 | 출력 | 실패 |
|-------|-----------|------|------|------|
| **UC-D01** | 빈칸 찾기 | UI 검증 통과 `Grid4x4` | `(r1,c1), (r2,c2)` row-major | 빈칸≠2 → UI에서 차단 |
| **UC-D02** | 누락 숫자 찾기 | `Grid4x4` | `MissingPair(small, large)` | present=14개 아님 → UI 차단; 차집합≠2 → `DomainError.INVALID_STATE` |
| **UC-D03** | 마방진 판정 | 빈칸 없는 `Grid4x4` | `true` / `false` | — |
| **UC-D04** | 두 조합 시도 | `PartialMagicGrid` | `SolutionTuple` | 두 조합 모두 false → `NO_COMPLETION` |
| **UC-D05** | 솔루션 해석 (오케스트레이션) | `Grid4x4` | `int[6]` | 위 실패 전파 |

**UC-D04 상세 알고리즘 (개념):**

```
1. (r1,c1), (r2,c2) ← EmptyCellScanner
2. (small, large) ← MissingNumberResolver
3. gridA ← grid with (r1,c1)=small, (r2,c2)=large
4. if MagicSquareJudge(gridA) → return [r1,c1,small,r2,c2,large]
5. gridB ← grid with (r1,c1)=large, (r2,c2)=small
6. if MagicSquareJudge(gridB) → return [r1,c1,large,r2,c2,small]
7. return NO_COMPLETION
```

---

## 1.4 Domain API (내부 계약)

> 표기: `Result<T>` = `{ ok: true, value: T }` | `{ ok: false, error: DomainError }`  
> `DomainError` enum: `INVALID_STATE`, `NO_COMPLETION`

| API | 시그니처 (개념) | 입력 전제 | 출력 | 실패 조건 |
|-----|----------------|-----------|------|-----------|
| **scanEmptyCells** | `Grid4x4 → Result<(CellCoordinate, CellCoordinate)>` | INV-G1~G4 | row-major 2좌표 | 빈칸≠2 |
| **resolveMissingNumbers** | `Grid4x4 → Result<MissingPair>` | INV-G1~G4 | `(small,large)` | 차집합 크기≠2 |
| **isMagicSquare** | `Grid4x4 → boolean` | 빈칸 없음 | true/false | 빈칸 존재 시 `INVALID_STATE` |
| **tryAssignment** | `(Grid4x4, c1, n1, c2, n2) → boolean` | c1,c2가 빈칸 | 채운 격자 magic 여부 | — |
| **solvePartialGrid** | `Grid4x4 → Result<SolutionTuple>` | INV-G1~G4 | `int[6]` | `NO_COMPLETION` |
| **toOutputArray** | `SolutionTuple → int[6]` | — | `[r1,c1,n1,r2,c2,n2]` | — |

**실패조건 명세:**

| error | 발생 API | 조건 |
|-------|----------|------|
| `INVALID_STATE` | scan/resolve/isMagic | Domain 전제 위반 (UI 우회 시) |
| `NO_COMPLETION` | solvePartialGrid | UC-D04 4·6단계 모두 false |

**출력 배열 불변식 (항상 참):**

- `len(result) == 6`
- `result[0],result[1],result[4],result[5] ∈ [1,4]`
- `{result[2], result[4]} == MissingPair` (집합 동일)
- 채운 격자가 INV-D3 만족

---

## 1.5 Domain 단위 테스트 설계 (RED 우선)

### TDD 사이클 순서 (Domain Track)

| # | Red 테스트 | Green 최소 조건 | 보호 Invariant |
|---|-----------|-----------------|----------------|
| 1 | `MagicSquareJudge_완성정답_true` | 10선 합=34 | INV-D3 |
| 2 | `MagicSquareJudge_행하나틀림_false` | 1행 합≠34 | INV-D3 |
| 3 | `EmptyCellScanner_rowMajor순서` | 고정 격자 2좌표 | INV-D2 |
| 4 | `MissingNumberResolver_두개반환` | (1,7) 등 | INV-D1 |
| 5 | `tryAssignment_정답배치_true` | 단일 배치 | INV-D3 |
| 6 | `solve_작은수첫빈칸_성공` | forward 순서 출력 | INV-D6,D7 |
| 7 | `solve_반대배치_성공` | reverse n1,n2 | INV-D7 |
| 8 | `solve_둘다실패_NO_COMPLETION` | error 반환 | NO_COMPLETION |

### 테스트 케이스 카탈로그

**기준 완성 마방진 (FIX-MAGIC):**

```
[16,  3,  2, 13]
[ 5, 10, 11,  8]
[ 9,  6,  7, 12]
[ 4, 15, 14,  1]
```

| TC-ID | 유형 | Given (4×4) | When | Then | Invariant |
|-------|------|-------------|------|------|-----------|
| **DT-01** | 정상 | FIX-MAGIC | isMagicSquare | true | INV-D3 |
| **DT-02** | 정상 | FIX-MAGIC r1c1=17 | isMagicSquare | false | INV-D3 |
| **DT-03** | 정상 | FIX에서 (3,3)=0,(4,4)=0 | scanEmptyCells | (3,3),(4,4) | INV-D2 |
| **DT-04** | 정상 | DT-03 격자 | resolveMissing | (1,7) | INV-D1 |
| **DT-05** | 정상 | DT-03 격자 | solvePartialGrid | `[3,3,1,4,4,7]` | INV-D6,D7 |
| **DT-06** | 정상 | FIX에서 (1,1)=0,(4,4)=0 | solvePartialGrid | `[1,1,16,4,4,1]` | INV-D7 |
| **DT-07** | 정상 | FIX에서 (2,2)=0,(2,3)=0 | solvePartialGrid | `[2,2,10,2,3,11]` | INV-D2,D7 |
| **DT-08** | 비정상 | FIX에서 (1,1)=0,(1,2)=0,(3,3)=0 | scanEmptyCells | INVALID_STATE | INV-G2 |
| **DT-09** | 비정상 | 1~14만 채움+빈칸2 | resolveMissing | INVALID_STATE | INV-D1 |
| **DT-10** | 비정상 | FIX에서 (1,1)=0,(2,2)=0, 잘못된 14개 | solvePartialGrid | NO_COMPLETION | UC-D04-7 |
| **DT-11** | 엣지 | FIX 1칸만 0→채움 불가 케이스 | isMagicSquare | false | INV-D3 |
| **DT-12** | 정상 | FIX r4 전부+3칸만 | isMagicSquare | 10선 각각 검증 | INV-D3 |

### Domain RED 체크리스트

- [ ] 모든 테스트는 `Grid4x4` 또는 `int[][]` → VO 변환만 사용 (I/O·파일·UI 없음)
- [ ] 각 TC는 Invariant ID 1개 이상 명시
- [ ] 실패 테스트는 `Result.error` 또는 `false`로 **정확히** 기대
- [ ] 출력 기대값은 `int[6]` 리터럴로 고정 (DT-05,06,07)

---

# 2) Screen Layer (UI Layer) 설계 (Boundary Layer)

## 2.1 사용자/호출자 관점 시나리오

| Step | 행위 | 책임 레이어 |
|------|------|-------------|
| S1 | 호출자가 `4×4 int[][]` 전달 | Screen Input |
| S2 | 크기·빈칸·범위·중복 검증 | Screen Validator |
| S3 | 검증 실패 → `ErrorResponse` 즉시 반환 (Domain 미호출) | Screen |
| S4 | 검증 성공 → `Domain.solvePartialGrid(grid)` 호출 | Screen → Domain |
| S5 | Domain `NO_COMPLETION` → `ErrorResponse` | Screen |
| S6 | Domain 성공 → `int[6]` → `SuccessResponse` | Screen Output |
| S7 | (선택) 결과를 Data Layer에 저장 | Screen → Data |

**흐름:**

```
[Caller] --int[4][4]--> [ScreenValidator]
                              |
                    fail -----+---- ok
                      |              |
              [ErrorResponse]   [Domain.solve]
                                      |
                            fail -----+---- ok
                              |              |
                      [ErrorResponse]   [SuccessResponse int[6]]
```

---

## 2.2 UI 계약 (외부 계약)

### Input Schema

| 필드 | 타입 | 제약 | 검증 순서 |
|------|------|------|-----------|
| `grid` | `int[4][4]` | non-null | 1 |
| `grid.length` | int | = 4 | 2 |
| `grid[r].length` | int | 각 행 = 4 | 2 |
| `grid[r][c]` | int | ∈ `{0} ∪ [1,16]` | 3 |
| `count(0)` | int | = 2 | 4 |
| non-zero values | set | size = count(non-zero) | 5 |

### Output Schema — Success

| 필드 | 타입 | 제약 |
|------|------|------|
| `status` | string | `"OK"` |
| `result` | `int[6]` | `[r1,c1,n1,r2,c2,n2]`, 좌표 1-index, Domain 출력 그대로 |

### Output Schema — Error

| 필드 | 타입 | 제약 |
|------|------|------|
| `status` | string | `"ERROR"` |
| `code` | string | Error Code 표 |
| `message` | string | 고정 문구 (`{value}` 치환만 허용) |

### Error Code 표

| code | 발생 조건 | message (고정) |
|------|-----------|----------------|
| `ERR_NULL_GRID` | grid == null | `Input grid is null.` |
| `ERR_GRID_ROWS` | row count ≠ 4 | `Grid must have exactly 4 rows.` |
| `ERR_GRID_COLS` | any row length ≠ 4 | `Each row must have exactly 4 columns.` |
| `ERR_VALUE_RANGE` | cell ∉ {0}∪[1,16] | `Cell value must be 0 or between 1 and 16 inclusive.` |
| `ERR_EMPTY_COUNT` | zero count ≠ 2 | `Grid must contain exactly 2 empty cells (value 0).` |
| `ERR_DUPLICATE` | non-zero duplicated | `Duplicate non-zero value: {value}.` |
| `ERR_NO_SOLUTION` | Domain NO_COMPLETION | `No magic square completion exists for the given grid.` |
| `ERR_INTERNAL` | Domain INVALID_STATE (우회) | `Internal domain error: invalid grid state.` |

**검증 단락 순서 (고정):**  
`NULL → ROWS → COLS → RANGE → EMPTY_COUNT → DUPLICATE`  
(첫 위반 1건만 반환)

---

## 2.3 UI 레벨 테스트 (Contract-first, RED 우선)

**전제:** Domain은 **Mock** (`solvePartialGrid`). Mock은 검증 통과 입력에 대해 `(int[6], error)`만 반환.

| TC-ID | Given | Mock | Then | 검증 계약 |
|-------|-------|------|------|-----------|
| **UT-01** | null | 미호출 | ERROR / ERR_NULL_GRID | Input |
| **UT-02** | 3×4 | 미호출 | ERROR / ERR_GRID_ROWS | Input |
| **UT-03** | 4×3 | 미호출 | ERROR / ERR_GRID_COLS | Input |
| **UT-04** | cell=17 | 미호출 | ERROR / ERR_VALUE_RANGE | Input |
| **UT-05** | cell=-1 | 미호출 | ERROR / ERR_VALUE_RANGE | Input |
| **UT-06** | zero×1 | 미호출 | ERROR / ERR_EMPTY_COUNT | Input |
| **UT-07** | zero×3 | 미호출 | ERROR / ERR_EMPTY_COUNT | Input |
| **UT-08** | two 5s | 미호출 | ERROR / ERR_DUPLICATE / `Duplicate non-zero value: 5.` | Input |
| **UT-09** | 유효 격자 | `[3,3,1,4,4,7]` | OK / result exact match | Output format |
| **UT-10** | 유효 격자 | NO_COMPLETION | ERROR / ERR_NO_SOLUTION | Domain bridge |
| **UT-11** | 유효 격자 | `[1,1,16,4,4,1]` | result.length=6, coords∈[1,4] | Output format |
| **UT-12** | 유효 격자 | Mock 미설정 | ERROR / ERR_INTERNAL if domain invalid | — |

**UT-09 Given (DT-03과 동일):**

```
[16,  3,  2, 13]
[ 5, 10, 11,  8]
[ 9,  6,  0, 12]
[ 4, 15, 14,  0]
```

### UI RED 체크리스트

- [ ] Domain Mock: `solvePartialGrid` 호출 횟수 = 검증 통과 시 1, 실패 시 0
- [ ] message 문자열 **완전 일치** assert (공백·대소문자 포함)
- [ ] result 배열 **요소별** assert (참조 동일성 아님)

---

## 2.4 UX/출력 규칙

| 규칙 ID | 규칙 |
|---------|------|
| **UX-01** | 성공 시 `status`는 반드시 `"OK"` (대문자) |
| **UX-02** | 실패 시 `status`는 반드시 `"ERROR"` |
| **UX-03** | 에러는 **첫 번째** 검증 위반 1건만 반환 |
| **UX-04** | `message`는 Error Code 표 문구와 **바이트 단위 동일** (`{value}` 치환만 예외) |
| **UX-05** | 성공 `result`는 Domain `int[6]` **변환·재정렬 금지** |
| **UX-06** | 좌표는 **1-index**; 0-index로 변환하지 않음 |
| **UX-07** | `ERR_DUPLICATE`의 `{value}` = 최초 탐지된 중복 non-zero (row-major) |

---

# 3) Data Layer 설계 (Data Layer)

## 3.1 목적 정의

| 항목 | 내용 |
|------|------|
| **필요성** | 동일 입력·결과 **재현**, TDD Refactor 단계에서 **영속성 교체** 연습 |
| **범위** | 입력 `int[4][4]` 저장·로드; (선택) 마지막 `int[6]` 결과 저장 |
| **비범위** | DB, ORM, 동시성, 버전 마이그레이션, UI 표시 |

---

## 3.2 인터페이스 계약

| 메서드 | 입력 | 출력 | 실패 |
|--------|------|------|------|
| `saveGrid(id: string, grid: int[4][4]) → void` | id non-empty, grid UI 계약 통과 | — | `DataError.INVALID_ID`, `DataError.INVALID_GRID` |
| `loadGrid(id: string) → int[4][4]` | id | 4×4 | `DataError.NOT_FOUND`, `DataError.CORRUPT` |
| `saveResult(id: string, result: int[6]) → void` | id exists, len=6 | — | `NOT_FOUND`, `INVALID_RESULT` |
| `loadResult(id: string) → int[6]` | id | 6원소 | `NOT_FOUND`, `CORRUPT` |
| `delete(id: string) → void` | id | — | idempotent (없어도 ok) |

**저장 레코드 (개념):**

```
Record { id, grid[4][4], result[6]?, savedAt ISO-8601 }
```

---

## 3.3 구현 옵션 비교 (메모리 / 파일)

| 항목 | A: InMemory | B: File (JSON) |
|------|-------------|----------------|
| 저장소 | `Map<string, Record>` | `{id}.json` |
| 속도 | 즉시 | I/O 지연 |
| TDD 난이도 | 최저 | 중간 (경로·파일 mock) |
| Refactor 연습 | Repository 인터페이스만 | **동일 인터페이스 뒤 구현 교체** |
| 프로세스 재시작 | 데이터 소실 | 유지 |
| 테스트 격리 | 인스턴스 per test | temp dir per test |

**추천: A (InMemory) → B (File) 2단계**

1. **1차 TDD:** InMemory로 RED-GREEN-REFACTOR 완료 (Data 테스트 80% 달성)
2. **Refactor Track:** File 구현으로 교체; **인터페이스·테스트 케이스 변경 금지**

**이유:** Dual-Track 목표가 레이어 분리이므로, 영속성 복잡도는 Domain/UI 안정 후 추가.

---

## 3.4 Data 레이어 테스트

| TC-ID | Given | When | Then |
|-------|-------|------|------|
| **ST-01** | empty repo | saveGrid("a", G) | loadGrid("a") == G |
| **ST-02** | saved "a" | saveResult("a", R) | loadResult("a") == R |
| **ST-03** | empty | loadGrid("x") | NOT_FOUND |
| **ST-04** | empty | loadResult("x") | NOT_FOUND |
| **ST-05** | — | saveGrid("", G) | INVALID_ID |
| **ST-06** | — | saveGrid("a", 3×4) | INVALID_GRID |
| **ST-07** | File impl | 파일 수동 삭제 후 load | CORRUPT |
| **ST-08** | saved G | loadGrid | 4×4, 각 행 길이 4 | INV-G1 |
| **ST-09** | round-trip | save→load 100회 | G unchanged | 무손실 |
| **ST-10** | delete "a" | loadGrid("a") | NOT_FOUND |

**G (표준 픽스처):** UT-09 Given 격자.

---

# 4) Integration & Verification (통합 및 검증)

## 4.1 통합 경로 정의

**의존성 방향 (Clean Architecture):**

```
Screen (UI Boundary)
    ↓ calls
Application (선택: SolveMagicSquareUseCase) — 얇은 오케스트레이션
    ↓ calls
Domain (MagicSquareJudge, SolutionAssigner, …)
    ↑ implements (interface)
Data (MatrixRepository)
```

| 레이어 | 의존 가능 | 의존 금지 |
|--------|-----------|-----------|
| Domain | Domain | Screen, Data, Framework |
| Screen | Domain(port), Data(port) | Domain 내부 클래스 직접 |
| Data | — | Domain, Screen |
| Application | Domain, Repository interface | 구체 File path |

**기본 통합 경로 (Application 생략 시):**

```
ScreenValidator → Domain.solvePartialGrid → ScreenResponse
ScreenValidator → MatrixRepository.saveGrid (선택, 성공 후)
```

**Application 포함 경로 (권장 Refactor 이후):**

```
Screen → SolveMagicSquareUseCase.execute(grid)
           ├→ Domain.solvePartialGrid
           └→ MatrixRepository.saveGrid + saveResult
```

---

## 4.2 통합 테스트 시나리오

### 정상 (≥2)

| IT-ID | 시나리오 | 입력 | 기대 |
|-------|----------|------|------|
| **IT-OK-01** | End-to-end solve | UT-09 Given | status=OK, result=`[3,3,1,4,4,7]` |
| **IT-OK-02** | Save after solve | IT-OK-01 + id="session1" | loadGrid==input, loadResult==output |
| **IT-OK-03** | Reverse assignment path | DT-06 입력 | OK + Domain 기대 배열 |

### 실패 (≥3)

| IT-ID | 시나리오 | 입력 | 기대 |
|-------|----------|------|------|
| **IT-FAIL-01** | 입력 오류 | zero×3 | ERROR / ERR_EMPTY_COUNT, Domain 0회 |
| **IT-FAIL-02** | Domain 실패 | DT-10 격자 | ERROR / ERR_NO_SOLUTION |
| **IT-FAIL-03** | Data 실패 | solve OK → loadResult("missing") | NOT_FOUND (Data API 직접) |
| **IT-FAIL-04** | 중복 | UT-08 | ERROR / ERR_DUPLICATE |
| **IT-FAIL-05** | File corrupt | File repo + 손상 JSON | loadGrid → CORRUPT |

---

## 4.3 회귀 보호 규칙

| 규칙 ID | 내용 |
|---------|------|
| **REG-01** | `int[6]` 출력 포맷 `[r1,c1,n1,r2,c2,n2]` 변경 시 **Major 버전** + 전 테스트 갱신 |
| **REG-02** | Error Code `message` 문구 변경 시 UI Contract 테스트(UT-01~08) 동시 갱신 |
| **REG-03** | Domain Invariant ID 삭제·완화 금지; 완화 시 DT/IT 전부 재검토 |
| **REG-04** | CI에서 Domain/UI/Data 테스트 **전부** Green 아니면 merge 금지 |
| **REG-05** | Refactor 시 **테스트 코드 변경 없이** Green 유지 (동작 변경 시 테스트 먼저 Red) |
| **REG-06** | Mock은 UI Track만; Integration Track은 **실 Domain** 사용 |

---

## 4.4 커버리지 목표

| 레이어 | 목표 | 측정 범위 | 미달 시 조치 |
|--------|------|-----------|--------------|
| **Domain Logic** | **≥ 95%** line | `MagicSquareJudge`, `EmptyCellScanner`, `MissingNumberResolver`, `SolutionAssigner` | DT 미충족 TC 추가 |
| **UI Boundary** | **≥ 85%** line | Validator, Response mapper, Error factory | UT 전 code path 1개 이상 |
| **Data** | **≥ 80%** line | Repository impl + error paths | ST-03~07 필수 |

**Dual-Track 병행 규칙:**

| Track | RED 범위 | Green 범위 |
|-------|----------|------------|
| Logic | DT-01 → DT-08 순 | Domain만 |
| UI | UT-01 → UT-06 순 | Validator + Mock Domain |
| Data | ST-01 → ST-03 순 | InMemory impl |
| Integration | IT-OK-01, IT-FAIL-01~02 | 전 레이어 실 구현 |

---

## 4.5 Traceability Matrix (필수)

| Concept (Invariant) | Rule | Use Case | Contract | Test | Component |
|---------------------|------|----------|----------|------|-----------|
| INV-G1 4×4 | UX 검증 순서 2 | — | Input grid 4×4 | UT-02, UT-03 | ScreenValidator |
| INV-G2 빈칸 2 | zero count=2 | — | ERR_EMPTY_COUNT | UT-06, UT-07 | ScreenValidator |
| INV-G3 값 범위 | 0∪[1,16] | — | ERR_VALUE_RANGE | UT-04, UT-05 | ScreenValidator |
| INV-G4 0 제외 유일 | duplicate scan | — | ERR_DUPLICATE | UT-08 | ScreenValidator |
| INV-D1 누락 2개 | set diff size=2 | UC-D02 | MissingPair | DT-04, DT-09 | MissingNumberResolver |
| INV-D2 빈칸 순서 | row-major | UC-D01 | (r1,c1),(r2,c2) | DT-03, DT-07 | EmptyCellScanner |
| INV-D3 합=34 | 10선 검사 | UC-D03 | isMagicSquare | DT-01, DT-02, DT-12 | MagicSquareJudge |
| INV-D6 출력 숫자 | n1,n2 ∈ missing | UC-D05 | int[6] | DT-05, UT-09 | SolutionAssigner |
| INV-D7 배치 규칙 | try forward then reverse | UC-D04 | solve output order | DT-05, DT-06, DT-07 | SolutionAssigner |
| NO_COMPLETION | both assign fail | UC-D04 | ERR_NO_SOLUTION | DT-10, UT-10, IT-FAIL-02 | Screen + Domain |
| Persistence | round-trip | save/load | MatrixRepository | ST-01, IT-OK-02 | InMemory/File Repository |
| Output format | no transform | UC-D05 | Success result[6] | UT-09, UT-11, IT-OK-01 | Screen ResponseMapper |
| Error wording | fixed message | UX-04 | Error schema | UT-01~08 | ErrorFactory |
| REG contract lock | format frozen | — | int[6] schema | IT-OK-01 | CI regression suite |

---

## 설계 완료 자체 검수 체크리스트

- [ ] 모든 Invariant (INV-G*, INV-D*)가 Test ID에 1:1 이상 매핑됨
- [ ] 입력·출력 계약에 모호어(“적절히”, “충분히”) 없음
- [ ] UI Error message 8종 문구 고정됨
- [ ] Domain·UI·Data 책임 겹침 없음 (검증 vs 판정 vs 저장)
- [ ] RED 우선 순서가 Logic/UI/Data 각각 명시됨
- [ ] 통합 정상 2+, 실패 3+ 시나리오 포함
- [ ] 커버리지 목표 Domain 95% / UI 85% / Data 80% 명시
- [ ] Traceability Matrix 14행 이상
- [ ] 구현 코드·프레임워크·클래스 파일 없음
- [ ] 좌표 1-index, 빈칸=`0`, Magic Constant=**34** 전 구간 일관

---

## 다음 단계 (구현 착수 전)

- [ ] Domain Track: **DT-01** Red 테스트 작성 → `MagicSquareJudge` 최소 Green
- [ ] UI Track: **UT-01** Red 테스트 + Mock Domain 병행
- [ ] Data Track: **ST-01** InMemory Repository Red → Green

---

## 부록: 참고 격자 (픽스처)

**FIX-MAGIC (완성 예시):**

```
[16,  3,  2, 13]
[ 5, 10, 11,  8]
[ 9,  6,  7, 12]
[ 4, 15, 14,  1]
```

**부분 입력 예시 (UT-09 / DT-03):**

```
[16,  3,  2, 13]
[ 5, 10, 11,  8]
[ 9,  6,  0, 12]
[ 4, 15, 14,  0]
```

**기대 출력:** `[3, 3, 1, 4, 4, 7]`
