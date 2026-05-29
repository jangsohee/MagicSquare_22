# Magic Square 4x4 — Dual-Track TDD design (transcript)
_Exported on 5/28/2026 from Cursor — TDD 설계 단계 대화 기록_

---

**User**

너는 Cursor.AI용 프롬프트 설계자다.
나는 Magic Square 4x4 TDD 설계 문서를 만들기 위한 프롬프트가 필요하다.
지금 설계 문서를 만들지 말고,그 설계 문서를 만들 수 있는 실행용 프롬프트만 작성하라.

---

**Cursor**

프로젝트 맥락(`README.md`, `Report/01-problem-definition-report.md`)을 확인한 뒤, 설계 문서 생성용 **실행 프롬프트**만 작성했습니다. (설계 문서 본문은 작성하지 않음)

**핵심 구조 요약:**
- 역할: TDD 설계 문서 작성 전문가
- 선행 문서: README + 01-problem-definition-report 상속
- 산출물: `Report/02-tdd-design-report.md` (문장 수준 입출력 계약, invariant→TC, Red-Green-Refactor 순서, 20+ TC, Traceability)
- 제외: 코드, 알고리즘, UI, 프레임워크
- 출력: Executive Summary 확인 후 전체 문서

**(실행 프롬프트 전문 — Cursor가 생성한 실행용 프롬프트)**

```markdown
# Magic Square 4×4 — TDD 설계 문서 작성 (실행 프롬프트)

당신은 **TDD 설계 문서 작성 전문가**이자, **규칙 기반 도메인 모델링**에 능숙한 소프트웨어 설계자입니다.
...

## 6. 시작
위 지시를 모두 이해했다면, **STEP 0**으로 `README.md`와 `Report/01-problem-definition-report.md`를 읽고,
**Executive Summary 초안**부터 작성하십시오.
```

> 전체 실행 프롬프트는 대화 당시 Cursor 응답 본문에 포함됨. 재사용 시 동일 User 메시지로 재생성 가능.

---

**User**

당신은 Dual-Track UI + Logic TDD 및 Clean Architecture 설계 전문가입니다.
프로젝트: Magic Square (4x4) — TDD 연습용
목적: 알고리즘 난이도보다 “레이어 분리 + 계약 기반 테스트 + 리팩토링” 훈련
제약:
- 구현 코드는 작성하지 마십시오. (설계/계약/테스트/통합 계획만)
- UI는 실제 화면이 아니라 “입력/출력 경계(Boundary)”로 정의
- Data Layer는 DB가 아니라 “저장/로드 인터페이스(메모리/파일 교체 가능)” 수준만
- 입력/출력은 명확히 고정
입력 계약:
- 4x4 int[][] (0은 빈칸)
- 빈칸은 정확히 2개
- 값 범위: 0 또는 1~16
- 0 제외 중복 금지
출력 계약:
- int[6]
- 좌표는 1-index
- 반환 형식: [r1,c1,n1,r2,c2,n2]
- n1,n2는 두 누락 숫자이며, (작은수→첫빈칸, 큰수→둘째빈칸) 조합이 마방진이면 그 순서로, 아니면 반대로

------------------------------------------------------------
출력 형식 (반드시 이 구조로)
------------------------------------------------------------
# 1) Logic Layer (Domain Layer) 설계
## 1.1 도메인 개념
...
# 4) Integration & Verification (통합 및 검증)
## 4.5 Traceability Matrix (필수)

------------------------------------------------------------
추가 조건
------------------------------------------------------------
- 모호한 표현 금지(“적절히/충분히” 금지)
- 모든 규칙은 검증 가능해야 함(테스트로 확인 가능)
- 구현 코드 작성 금지
- 표/체크리스트를 적극 사용
```

---

**Cursor**

`Report/01-problem-definition-report.md`의 invariant(행·열·대각 합 일치, Magic Constant=34)와 사용자가 고정한 입출력 계약을 전제로, **Dual-Track UI + Logic TDD + Clean Architecture** 설계 문서를 작성했습니다.

**고정 계약 요약:**
| 항목 | 내용 |
|------|------|
| 입력 | `4×4 int[][]`, `0`=빈칸×2, 값 `0` 또는 `1~16`, 0 제외 중복 금지 |
| 출력 | `int[6]` = `[r1,c1,n1,r2,c2,n2]` (1-index) |
| 배치 규칙 | 작→첫빈·큰→둘째 magic이면 그 순서, 아니면 n1,n2 반대 |
| Magic Constant | **34** |

**설계 산출물 구조:**
1. **Logic Layer** — Grid4x4, EmptyCellScanner, MissingNumberResolver, MagicSquareJudge, SolutionAssigner; INV-G*/INV-D*; Domain API; DT-01~12
2. **Screen Layer** — Validator 단락 순서, Error Code 8종 고정 message, UT-01~12 (Domain Mock)
3. **Data Layer** — MatrixRepository save/load; InMemory→File 2단계; ST-01~10
4. **Integration** — 의존성 방향, IT-OK/FAIL 시나리오, 커버리지 95/85/80%, Traceability Matrix 14행

> **전문:** `Report/02-tdd-design-report.md` (본 Export 이후 저장됨)

---

**User**

다음의 순서로 실행해줘
1. Report 폴더에 보고서 생성해줘
2. 현재까지의 프롬프트 전체를 대화형 프롬프트로 Prompt 폴더에 Export transcript 해줘

---

**Cursor**

1. `Report/02-tdd-design-report.md` 생성 — Dual-Track TDD 설계 보고서 전문 저장
2. `Prompting/02-tdd-design-prompt.md` 생성 — 본 파일 (대화 Transcript Export)

**생성 파일:**

| 파일 | 설명 |
|------|------|
| `Report/02-tdd-design-report.md` | Logic / Screen / Data / Integration 설계·계약·테스트·Traceability Matrix |
| `Prompting/02-tdd-design-prompt.md` | TDD 설계 단계 User↔Cursor 대화 Export |

---

## 재사용 가이드 (대화형 프롬프트)

아래 순서로 Cursor에 붙여 넣으면 동일 흐름을 재현할 수 있습니다.

### Turn 1 — (선택) TDD 설계 실행 프롬프트 생성

```
너는 Cursor.AI용 프롬프트 설계자다.
나는 Magic Square 4x4 TDD 설계 문서를 만들기 위한 프롬프트가 필요하다.
지금 설계 문서를 만들지 말고, 그 설계 문서를 만들 수 있는 실행용 프롬프트만 작성하라.
```

### Turn 2 — Dual-Track TDD 설계 (핵심)

```
당신은 Dual-Track UI + Logic TDD 및 Clean Architecture 설계 전문가입니다.
프로젝트: Magic Square (4x4) — TDD 연습용
목적: 알고리즘 난이도보다 “레이어 분리 + 계약 기반 테스트 + 리팩토링” 훈련
제약:
- 구현 코드는 작성하지 마십시오. (설계/계약/테스트/통합 계획만)
- UI는 실제 화면이 아니라 “입력/출력 경계(Boundary)”로 정의
- Data Layer는 DB가 아니라 “저장/로드 인터페이스(메모리/파일 교체 가능)” 수준만
- 입력/출력은 명확히 고정
입력 계약:
- 4x4 int[][] (0은 빈칸)
- 빈칸은 정확히 2개
- 값 범위: 0 또는 1~16
- 0 제외 중복 금지
출력 계약:
- int[6]
- 좌표는 1-index
- 반환 형식: [r1,c1,n1,r2,c2,n2]
- n1,n2는 두 누락 숫자이며, (작은수→첫빈칸, 큰수→둘째빈칸) 조합이 마방진이면 그 순서로, 아니면 반대로

(출력 형식 섹션 1~4 및 Traceability Matrix, 추가 조건 포함 — User 메시지 전문 참조)

선행 문서: Report/01-problem-definition-report.md 를 읽고 invariant를 상속하라.
```

### Turn 3 — 저장

```
다음의 순서로 실행해줘
1. Report 폴더에 보고서 생성해줘
2. 현재까지의 프롬프트 전체를 대화형 프롬프트로 Prompting 폴더에 Export transcript 해줘
```

---

## 관련 산출물

| 문서 | 경로 |
|------|------|
| 문제 정의 보고서 | `Report/01-problem-definition-report.md` |
| TDD 설계 보고서 | `Report/02-tdd-design-report.md` |
| 문제 정의 Transcript | `Prompting/01-problem-definition-prompt.md` |
| TDD 설계 Transcript | `Prompting/02-tdd-design-prompt.md` (본 파일) |
