# Magic Square — Dual-Track RED 설계 (transcript)
_Exported on 2026-05-29 from Cursor — FR-01~05 RED 설계표 작성 → Report/09 Export_  
_선행: `Report/02`, `docs/PRD_MagicSquare.md`, `docs/test_plan.md`, `Report/08`, `.cursorrules`_

---

**User**

Dual-Track UI + Logic TDD 전문가 역할.

**TDD phase: RED** — 오직 RED 테스트 설계표만 작성.

**금지:** 구현/테스트/스켈레톤 코드, 클래스·파일 구조 확정, GREEN/REFACTOR, pytest 실행, 파일 저장.

**SSOT:** PRD v0.2, Report/02, .cursorrules

**계약 요약:**
- 4×4, 0×2, int[6] 1-index, M=34
- Short-circuit: null → size → empty count → range → duplicate
- Boundary: E003/E001/E002/E004/E005 Failure envelope; invalid 시 `SolvePartialMagicSquare.execute` 0회 (U-FLOW-02)
- Domain: Mock 금지

**범위:** FR-01~FR-05 Dual-Track RED 설계표

**Track A:** U-IN-* (null, size 3×4/4×3/5×5/[], empty 0·3, range -1·17, duplicate), U-OUT-* (len 6, 1-index), U-FLOW-02

**Track B:** find_blank_coords, find_not_exist_nums, is_magic_square (G0~분리 false), solution (G1/G2/G3); G0~G3; D-LOC/MIS/VAL/SOL IDs; I1~I11

**출력 형식:** UI RED Tests 표 + Logic RED Tests 표 + 검수 체크리스트

---

**Cursor**

**TDD phase: RED** 설계표 출력 (코드·파일 저장 없음).

**Track A — 14건**
- U-IN-01~05: 입력 검증 + execute 0회
- U-OUT-01~02: G1 기준 int[6]·1-index
- U-FLOW-02: invalid 시 execute call_count==0

**Track B — 12건**
- D-LOC-01, D-MIS-01, D-VAL-01~06, D-SOL-01~04
- Domain Mock 금지 명시

**격자:**
- G0 = FIX-MAGIC
- G1 = v0.2 (2,2)(3,3) placeholder — Report DT-03과 불일치 명시
- G2 = DT-06, G3 = DT-10

**Traceability:** E003↔ERR_NULL_GRID 등 매핑 표기

**검수 6항목 Pass**

**권장 순서:** U-IN-01+U-FLOW-02 ∥ D-VAL-01 → …

---

**User**

Report 폴더에 보고서 생성하고, Prompting 폴더에 Transcript Export.

---

**Cursor**

- `Report/09-dual-track-red-design-report.md` — Executive Summary, STEP 1~6, Traceability, 교차 이슈
- `Prompting/09-dual-track-red-design-prompt.md` (본 문서)
- `README.md` — Report/09, Prompting/09, 진행 상황 갱신

---

## 재사용 프롬프트 (Dual-Track RED 설계표)

```markdown
TDD phase: RED only — Dual-Track 설계표

금지: 코드, pytest, 파일 저장, GREEN/REFACTOR

Track A (Boundary):
- U-IN: null→E003, size→E001, empty→E002, range→E004, dup→E005
- U-OUT: len 6, coords 1-index (valid G1)
- U-FLOW-02: execute call_count==0 on invalid

Track B (Domain, no Mock):
- D-LOC, D-MIS, D-VAL-01~06, D-SOL-01~04
- G0 FIX-MAGIC, G1/G2/G3 per Report/02 or v0.2 appendix

각 행: Test ID, Layer, 이름, Given, When, Then, Expected RED Failure, Invariant/AC

출력: # UI RED Tests 표 + # Logic RED Tests 표 + 체크리스트
SSOT: Report/02, PRD, .cursorrules
```

---

## 관련 문서

| 문서 | 경로 |
|------|------|
| 본 단계 보고서 | `Report/09-dual-track-red-design-report.md` |
| 테스트 플랜·RED QA | `Report/08-test-plan-red-phase-report.md` |
| TDD 설계 SSOT | `Report/02-tdd-design-report.md` |
| 결함 목록 | `defect_list.md` |
