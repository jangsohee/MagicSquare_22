# Magic Square — Dual-Track RED Skeleton (transcript)
_Exported on 2026-05-29 from Cursor — Report/09 설계표 → pytest RED Skeleton 작성 → Report/10 Export_  
_선행: `Report/09`, `docs/PRD_MagicSquare.md`, `Report/02`, `Report/08`, `.cursorrules`_

---

**User**

Dual-Track UI + Logic TDD 전문가 역할.

**TDD phase: RED (Skeleton)** — 테스트 스켈레톤만 작성.

**SSOT:** Report/09, PRD v0.2, Report/02, .cursorrules

**금지:** src/ 구현, GREEN/REFACTOR, skip/xfail, assert Then, Report/08 13건 수정

**범위 (pytest 없는 항목만):**
- Track A: U-IN-04~08, U-OUT-01~03, U-FLOW-02(확장)
- Track B: D-LOC-01, D-MIS-01, D-VAL-01~06, D-SOL-01~04
- U-IN-01~03 중복 금지

**RED Skeleton 규칙:**
- 구조·import·fixture placeholder만
- 본문 = `pytest.fail("RED: <ID> — …")` 한 줄
- Arrange/Act 주석만; Then assert 없음
- G0~G3 conftest 주석 placeholder; D-SOL-02 → G2 TBD

**완료 조건:** `pytest tests/boundary/ tests/entity/` 전부 RED, src/ 변경 없음

---

**Cursor**

Report/09·기존 테스트 패턴 확인 후 RED Skeleton 10파일·21건 작성.

**Track A — 9건**
- `test_u_in_04_value_range.py` — U-IN-04a (cell=17), U-IN-04b (cell=-1)
- `test_u_in_05_duplicate.py` — U-IN-05 (duplicate 5)
- `test_u_out_output_contract.py` — U-OUT-01 (len 6), 02 (1-index), 03 (G1 tuple passthrough 확장)
- `test_u_flow_02_execute_isolation.py` — U-FLOW-02 null + ext E004/E005 execute 0회 spy 주석

**Track B — 12건**
- `test_d_loc_01.py`, `test_d_mis_01.py`, `test_d_val.py` (6), `test_d_sol.py` (4)
- Domain Mock 금지; import `magicsquare.entity.services.*`

**Fixture**
- `tests/conftest.py` — G0~G3 리터럴·fixture 주석
- `tests/entity/conftest.py` — entity placeholder

**범위 메모**
- Report/09 SSOT: U-IN-04a/b·05까지만 정의 → U-IN-06~08 생략
- U-OUT-03: 요청 범위 확장 (Report/09에 없음)
- Report/08 `test_ac_fr01_01_null_grid.py` assert 불변

**pytest 결과**
```
python -m pytest tests/boundary/ tests/entity/ -v
→ 9 errors, 수집 중단 (passed 0)

python -m pytest ... --continue-on-collection-errors
→ 9 passed (test_user.py), 9 errors (boundary + test_d_*)
```

- boundary: `ModuleNotFoundError: magicsquare.boundary`
- entity D-*: `ModuleNotFoundError: magicsquare.entity.services`
- src/ 변경 없음

---

**User**

Report 폴더에 보고서 생성하고, Prompting 폴더에 Transcript도 Export 해줘

---

**Cursor**

- `Report/10-dual-track-red-skeleton-report.md` — Executive Summary, STEP 1~7, Traceability, pytest 검증, 교차 이슈
- `Prompting/10-dual-track-red-skeleton-prompt.md` (본 문서)
- `README.md` — Report/10, Prompting/10, 진행 상황 갱신

---

## 재사용 프롬프트 (Dual-Track RED Skeleton)

```markdown
TDD phase: RED (Skeleton) only

금지: src/, GREEN, REFACTOR, skip, xfail, assert Then, Report/08 수정

SSOT: Report/09, Report/02, PRD, .cursorrules

범위: Report/09 중 pytest 없는 Test ID만
- Track A: tests/boundary/test_u_*.py
- Track B: tests/entity/test_d_*.py (Domain Mock 금지)

규칙:
- test_<test_id>_<scenario>
- 본문: pytest.fail("RED: <ID> — <한 줄 설계>")
- Given/When/Then 주석만
- G0~G3: tests/conftest.py placeholder

완료: pytest boundary+entity RED, src/ 무변경
```

---

## 관련 문서

| 문서 | 경로 |
|------|------|
| 본 단계 보고서 | `Report/10-dual-track-red-skeleton-report.md` |
| RED 설계표 | `Report/09-dual-track-red-design-report.md` |
| 테스트 플랜·RED QA | `Report/08-test-plan-red-phase-report.md` |
| TDD 설계 SSOT | `Report/02-tdd-design-report.md` |
| 결함 목록 | `defect_list.md` |
