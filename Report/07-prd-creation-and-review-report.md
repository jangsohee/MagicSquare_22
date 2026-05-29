# Magic Square 프로젝트 — PRD 작성·검토 보고서

**작성 목적:** 구현 전 PRD(`docs/PRD_MagicSquare.md`) 작성, 저장, 7항목 기준 검토 결과를 한 흐름으로 정리  
**대상:** 주니어 개발자 + Cursor AI 협업 학습 프로젝트  
**범위:** 참고 문서 분석·매핑 → PRD 본문(§1~§23) → 저장 → 검토 보고 (구현·테스트 코드 제외)  
**선행 문서:** `Report/01-problem-definition-report.md`, `Report/02-tdd-design-report.md`, `Report/06-user-journey-to-scenario-verification-report.md`, `Report/03-cursor-rules-and-implementation-report.md`  
**작성일:** 2026-05-28

---

## Executive Summary

본 단계에서 MagicSquare 4×4 TDD Practice는 **구현 전 기준 문서(PRD)** 를 완성했다. 선행 단계의 참고 문서 6종을 분석·매핑한 뒤, Dual-Track·ECB·Traceability를 반영한 PRD 본문(23절)을 작성하고 `docs/PRD_MagicSquare.md`에 저장했다. 이어 7항목 기준으로 PRD를 검토하여 **구현 착수 가능(조건부)** 판정과 P0~P2 개선 권장 사항을 고정했다.

| 항목 | 결과 |
|------|------|
| **PRD 파일** | `docs/PRD_MagicSquare.md` (v1.0 Draft) |
| **참고 문서 매핑** | Report/01·02·03·06 + `.cursorrules` + `magicsquare-*.mdc` |
| **7항목 검토** | 5항목 충족·2항목 부분 충족 (AC 완전성, Traceability AC-ID) |
| **오류 정책 (NO_COMPLETION)** | PRD 내 **확정** (`ERR_NO_SOLUTION`, 예외 미던짐) |
| **DEC 미해결** | DEC-01~06 (레이어 배치, Data MVP, Persona 등) |
| **`src/` 마방진 핵심 (DT-01~)** | 미착수 (변경 없음) |

**pytest:** `9 passed` (변경 없음 — `tests/entity/test_user.py`)

**Transcript:** `Prompting/07-prd-creation-and-review-prompt.md`

---

## STEP 1 — PRD 참고 문서 분석 및 매핑

### 1.1 요청

- PRD 본문 작성 **전** 참고 문서 6종 분석
- PRD 섹션별 Primary/Secondary Source, 출처 우선순위, 본문 vs 부록 구분
- 권장 PRD 목차(§8)만 제시 — **본문·파일 미작성**

### 1.2 워크스페이스 경로 매핑

| 요청 문서명 | 실제 경로 |
|-------------|-----------|
| Report/1 Problem Definition | `Report/01-problem-definition-report.md` |
| Report/2 Clean Architecture / TDD Design | `Report/02-tdd-design-report.md` |
| Report/3 Dev Environment / Cursor Rules | `Report/03-cursor-rules-and-implementation-report.md` |
| Report/4 User Journey → Scenario | `Report/06-user-journey-to-scenario-verification-report.md` |
| Cursor rules | `.cursorrules`, `.cursor/rules/magicsquare-*.mdc` |

### 1.3 핵심 판단

| 항목 | 내용 |
|------|------|
| PRD 작성 가능 여부 | **가능 (조건부)** |
| 1차 참고 (요구·검증) | `Report/06` + 계약 SSOT `Report/02` |
| 누락 정보 | Mom Test 사용자 확정, UI 형태, DEC-01 레이어 harmonization |

### 1.4 출처 우선순위 (고정)

| 주제 | Primary |
|------|---------|
| I/O·Error·Invariant·TC-ID | Report/02 |
| Epic·Story·AC·Gherkin | Report/06 |
| Background·Why Chain | Report/01 |
| Engineering·TDD·금지 패턴 | Report/03 + Cursor Rules |

---

## STEP 2 — PRD 본문 작성 및 저장

### 2.1 요청

- Senior Product/Software Architect 역할로 **구현 전 PRD** 작성
- §1~§23 고정 구조, Dual-Track, Traceability Matrix 필수
- 모호어 금지, 테스트 가능한 AC, 코드·테스트·파일 생성 금지(당시)

### 2.2 산출물 구조

| 섹션 | 핵심 내용 |
|------|-----------|
| §1~§8 | Executive Summary, Background, Problem, Why, Users, Vision, Journey |
| §9 | In/Out of Scope |
| §10 | FR-01~FR-05 (Boundary 검증, Blank, Missing, Judge, Solver) |
| §11~§13 | BR-01~16, I/O Contract, Error Policy (**NO_COMPLETION 확정**) |
| §14~§16 | NFR, Dual-Track TDD, Test Plan |
| §17~§18 | ECB Architecture, Component Candidates |
| §19~§22 | Risks, Engineering Principles, Traceability, DEC-01~06 |
| §23 | Appendix (Gherkin 요약, RED 순서, DoD) |

### 2.3 고정 계약 (PRD 반영)

| 항목 | 값 |
|------|-----|
| 입력 | 4×4, `0`=빈칸×2, `0` 또는 1~16, 0 제외 중복 금지 |
| 출력 | `int[6]` = `[r1,c1,n1,r2,c2,n2]`, **1-index** |
| 배치 | small-first → reverse, 실패 시 `ERR_NO_SOLUTION` |
| Magic Constant | 10선 합 = **34** (`TARGET_LINE_SUM` 단일 출처) |
| Boundary 검증 순서 | NULL → ROWS → COLS → RANGE → EMPTY_COUNT → DUPLICATE |

### 2.4 저장

| 파일 | 설명 |
|------|------|
| `docs/PRD_MagicSquare.md` | PRD v1.0 Draft 전문 |

---

## STEP 3 — PRD 7항목 검토

### 3.1 검토 기준별 판정

| # | 기준 | 판정 | 심각도 |
|---|------|------|--------|
| 1 | FR별 테스트 가능 AC | 부분 충족 | 중 |
| 2 | AC ↔ Traceability Matrix | 부분 충족 | 중 |
| 3 | Boundary/Domain 분리 | 대체로 충족, 용어·배치 모호 | 중 |
| 4 | 오류 정책 미정 | 핵심 확정, Domain 전달 방식 문서화 부족 | 낮~중 |
| 5 | small-first / reverse 데이터 구분 | 충족 | 낮 |
| 6 | 1-index / row-major | 충족, 대각·스캔 정의 보강 여지 | 낮 |
| 7 | 구현/테스트 코드 미포함 | 충족 | — |

### 3.2 주요 발견 (요약)

**AC·FR**

- FR-02/04/05: DT-07, DT-12 등 Related Test는 있으나 **전용 AC 누락**
- AC-FR05-05: MissingPair 검증에 **Given 격자 미지정**
- AC-FR01-04/05: UT-05, UT-07이 AC 문장에 미명시

**Traceability**

- §21은 Invariant 중심; **AC-ID 전수 매핑 표 없음**
- AC-FR01-07, AC-FR03-02, ERR_INTERNAL(UT-12) 등 Matrix 행 부재

**레이어**

- §1·FR 제목의 “Domain” vs ECB **Control+Entity** vs DEC-01 미해결 — 표면 모순
- Component `Control/Domain` 이중 표기

**오류**

- Boundary/NO_COMPLETION: **확정**
- Domain API `Result` vs `throw`, Data layer Error: **보강 권장**

**테스트 데이터**

- §12.4 `G_PARTIAL_FWD` / `G_SOL_REVERSE` 구분 양호
- DT-06/07 격자 ID 보강 권장

### 3.3 교차 이슈

| ID | 설명 |
|----|------|
| X-01 | §1 “§21에서 추적성 보장” ↔ AC 누락 |
| X-02 | DEC-01 미해결 vs FR Layer 단수 표기 |
| X-05 | `tests/entity/` vs Control 오케스트레이션 경로 불일치 |

### 3.4 우선순위별 개선 권장 (PRD 개정 시)

| 우선순위 | 작업 |
|----------|------|
| **P0** | §21 AC-ID 전수 매핑 표 추가 |
| **P0** | DEC-01 반영 후 FR Layer·§1 문구 정렬 |
| **P1** | 누락 AC (DT-07, DT-12, AC-FR05-05 Given), §13 Result 정책 |
| **P2** | BR-05a/BR-09a, §12.4 DT-06/07 격자 ID, FR-06 또는 Data Out-of-Scope 명시 |

---

## Traceability (본 단계)

| 단계 | 산출물 | Report/02 연계 |
|------|--------|------------------|
| 참고 분석 | 매핑 표 8절 | TC-ID·Error·INV SSOT |
| PRD 작성 | `docs/PRD_MagicSquare.md` | FR↔UT/DT/IT, §21 Matrix |
| PRD 검토 | 7항목 보고 | P0~P2 → Report/02·PRD v1.1 후보 |

---

## 문서 관계

```
Report/01 (Problem) ──► PRD §2~§4
Report/06 (Journey)  ──► PRD §6~§8, §10 AC
Report/02 (Design)   ──► PRD §10~§13, §21 (SSOT)
Report/03 + Rules    ──► PRD §14~§15, §20
docs/PRD_MagicSquare.md ──► 구현·Red 테스트 착수 기준 (DEC 해소 후)
```

---

## 다음 단계 (권장)

- [ ] DEC-01 확정: Judge/Solver **entity vs control** 배치
- [ ] PRD v1.1: P0~P1 반영 (AC-ID Matrix, Layer 용어 통일)
- [ ] `README.md`에 `docs/PRD_MagicSquare.md` 링크 추가 (선택)
- [ ] **DT-01** 또는 **UT-04** Red 착수 (PRD·Report/02 정합 확인 후)

---

## 변경 이력

| 날짜 | 내용 |
|------|------|
| 2026-05-28 | 참고 문서 분석 → PRD 작성 → `docs/PRD` 저장 → 7항목 검토 → Report/07·Prompting/07 Export |

---

## 부록 A — 생성·갱신 파일

| 경로 | 설명 |
|------|------|
| `docs/PRD_MagicSquare.md` | PRD v1.0 Draft |
| `Report/07-prd-creation-and-review-report.md` | 본 보고서 |
| `Prompting/07-prd-creation-and-review-prompt.md` | Transcript Export |

## 부록 B — 관련 문서

| 문서 | 경로 |
|------|------|
| TDD 설계 (TC-ID SSOT) | `Report/02-tdd-design-report.md` |
| User Journey 검증 | `Report/06-user-journey-to-scenario-verification-report.md` |
| 문제 정의 | `Report/01-problem-definition-report.md` |
| Cursor Rules | `.cursorrules`, `.cursor/rules/magicsquare-*.mdc` |
