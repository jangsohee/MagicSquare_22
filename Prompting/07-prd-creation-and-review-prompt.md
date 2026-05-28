# Magic Square — PRD 작성·검토 (transcript)
_Exported on 2026-05-28 from Cursor — PRD 참고 분석 → PRD 본문 → 저장 → 7항목 검토 대화 기록_  
_선행: `Report/01`~`06`, `Report/02-tdd-design-report.md` (계약 SSOT)_

---

**User**

PRD 작성 전문가·Dual-Track UI + Logic TDD 기반 제품 기획자 역할.

목표: Magic Square 4×4 구현 전 PRD 작성 — **지금은 PRD 본문 작성하지 말 것**.

참고 문서 6종 분석 및 PRD 섹션 매핑만 수행:
- Report/1 Problem Definition → Background, Why Chain
- Report/4 User Journey → Vision, Epic, Story, AC, Gherkin
- Report/2 Design → Contract, Invariant, Layer
- Report/3 + Cursor Rules → Quality, Engineering
- 중복 시 출처 우선순위, 본문 vs 부록 구분
- 권장 PRD 목차만 (§8)

제약: 코드·테스트·파일 수정·PRD 본문 작성 금지.

출력: `# PRD Reference Document Analysis` (§1~§8 고정 형식)

---

**Cursor**

워크스페이스 Report·Rules 파일 읽기 및 매핑 분석 수행 (파일 미생성).

**요청명 → 실제 경로:**

| 요청 | 실제 |
|------|------|
| Report/4 User Journey | `Report/06-user-journey-to-scenario-verification-report.md` |
| Report/2 Design | `Report/02-tdd-design-report.md` |
| 기타 | `Report/01`, `03`, `.cursorrules`, `magicsquare-*.mdc` |

**§1 Overall Judgment**

- PRD 작성: **가능 (조건부)**
- 1차 참고: Report/06 (요구·검증) + Report/02 (계약 SSOT)
- 누락: Mom Test 사용자, UI 형태, DEC-01 레이어 harmonization

**§4 Source Priority:** I/O·Error·INV → Report/02; Epic·Story → Report/06; Background → Report/01; Engineering → Report/03 + Rules

**§7 Conflicts:** Report/02 Screen/Domain vs ECB boundary/control/entity; L4 Gherkin incomplete; RED-* vs UT/DT 이중 체계

**§8 Recommended Outline:** §1~§23 (Executive → Appendix, Traceability, DEC)

---

**User**

Senior Product/Software Architect — **PRD 본문 작성** (구현 전 기준).

- Dual-Track (A: Boundary, B: Domain), Concept→Test Traceability
- 고정 I/O: 4×4, 0×2, int[6] 1-index, small-first→reverse, Magic=34
- 두 조합 실패 시 정책 **반드시 확정**
- §1~§23 구조, FR-01~05, BR, §21 Matrix
- 코드·테스트·**파일 생성 금지** — Markdown 본문만 (나중에 `docs/PRD_MagicSquare.md` 저장 예정)

출처 우선: Report/4 > Report/1 > Report/2 > Report/3; 충돌 시 Decision Needed.

---

**Cursor**

`docs/PRD_MagicSquare.md`에 저장 가능한 **PRD 전문** Markdown 출력 (§1~§23).

**핵심 확정:**

| 항목 | PRD 내용 |
|------|----------|
| 실패 (두 조합) | `NO_COMPLETION` → Boundary `ERR_NO_SOLUTION`, **예외 미던짐** |
| Boundary 실패 | Domain resolver **0회** |
| FR | FR-01 Boundary 검증, FR-02~05 Logic (Blank/Missing/Judge/Solver) |
| BR | BR-01~16 (4×4, 빈칸2, row-major, 1-index, int[6], …) |
| NFR | Domain ≥95%, Boundary ≥85%, Deterministic, 50ms, no input mutation |
| DEC | DEC-01~06 (레이어 배치, Data MVP, Persona, RED alias, User Entity) |
| §12.4 | G_PARTIAL_FWD `[3,3,1,4,4,7]`, G_SOL_REVERSE `[3,3,6,4,4,1]` |
| §21 | Invariant → FR → AC → TC → Component (18행+) |

---

**User**

PRD 본문(`docs/PRD_MagicSquare.md`)은 아직 파일로 저장합니다.

---

**Cursor**

`docs/` 디렉터리 생성 후 **`docs/PRD_MagicSquare.md`** 에 PRD v1.0 Draft 전문 저장 완료.

---

**User**

방금 작성한 PRD 검토 — **수정하지 말고** 문제·개선안만 보고.

7항목:
1. FR별 테스트 가능 AC
2. AC ↔ Traceability Matrix
3. Boundary/Domain 책임 혼합
4. 오류 정책 미정
5. small-first / reverse 데이터 구분
6. 1-index / row-major 누락
7. 구현·테스트 코드 포함 여부

---

**Cursor**

`docs/PRD_MagicSquare.md` 전문 대조 검토 보고 (수정 없음).

**요약 판정**

| # | 기준 | 판정 |
|---|------|------|
| 1 | FR별 AC | 부분 충족 (DT-07/12 AC 누락, AC-FR05-05 Given 없음) |
| 2 | Matrix 연결 | 부분 충족 (AC-ID 전수 매핑 없음) |
| 3 | 레이어 분리 | 대체로 충족 (Domain vs Control 용어 혼재, DEC-01) |
| 4 | 오류 정책 | 핵심 확정; Result vs throw 문서화 부족 |
| 5 | 테스트 데이터 | 충족 (G_PARTIAL_FWD / G_SOL_REVERSE) |
| 6 | 1-index / row-major | 충족 (대각 셀 정의 보강 여지) |
| 7 | 코드 미포함 | 충족 (§23.3 Gherkin은 명세) |

**P0 개선:** §21 AC-ID 전수 표; DEC-01 후 FR Layer 정렬  
**P1:** DT-07/12 AC, §13 Domain Result 정책  
**교차:** X-01 §1 “추적성 보장” 과장; X-05 tests/entity vs control 경로

---

**User**

Report 폴더에 보고서 생성하고, Prompting 폴더에 Transcript도 Export 해줘

---

**Cursor**

Level 1~3 산출물(참고 분석·PRD·검토) 통합 Export:

| 파일 | 설명 |
|------|------|
| `Report/07-prd-creation-and-review-report.md` | 본 단계 통합 보고서 |
| `Prompting/07-prd-creation-and-review-prompt.md` | 본 Transcript |

**Report/07 구성:**

- Executive Summary (PRD 저장, 7항목 검토, DEC-01~06, DT-01 미착수)
- STEP 1 참고 문서 분석·매핑
- STEP 2 PRD §1~§23 및 `docs/PRD_MagicSquare.md`
- STEP 3 7항목 검토·P0~P2·교차 이슈
- Traceability · 다음 단계 · 부록

**구현 상태:** `src/` 마방진 핵심 변경 없음 — 문서 Export만 수행

---

## 재사용 프롬프트 (PRD 일괄)

```markdown
Magic Square 4×4 — 구현 전 PRD

Phase A — 참고 문서만 분석·매핑 (PRD 본문·파일 금지)
- Report/01, 02, 03, 06 + .cursorrules + magicsquare-*.mdc
- 출력: PRD Reference Document Analysis §1~§8

Phase B — PRD 본문 §1~§23
- Dual-Track A(Boundary) / B(Domain)
- FR-01~05, BR, I/O, Error (NO_COMPLETION → ERR_NO_SOLUTION 확정)
- Traceability Matrix, DEC-01~06
- 모호어 금지, 테스트 가능 AC

Phase C — 저장: docs/PRD_MagicSquare.md

Phase D — 7항목 검토 (수정 없이 보고만)
1~7: AC, Matrix, Layer, Error, test data, 1-index, no code

Phase E — Report/07 + Prompting/07 Export

제약: 알고리즘 확장·N×N·UI/DB/Web Out-of-Scope
SSOT: Report/02 (계약·TC-ID), Report/06 (Epic·Story·AC)
```

---

## 관련 문서

| 문서 | 경로 |
|------|------|
| 본 단계 보고서 | `Report/07-prd-creation-and-review-report.md` |
| PRD 본문 | `docs/PRD_MagicSquare.md` |
| TDD 설계 (TC-ID) | `Report/02-tdd-design-report.md` |
| User Journey | `Report/06-user-journey-to-scenario-verification-report.md` |
| 문제 정의 | `Report/01-problem-definition-report.md` |
