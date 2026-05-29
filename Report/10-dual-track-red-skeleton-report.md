# Magic Square 프로젝트 — Dual-Track RED Skeleton 보고서

**작성 목적:** Report/09 설계표 기반 **RED Skeleton** pytest 파일 작성·검증 결과를 Dual-Track(UI Boundary / Domain Logic)으로 정리  
**대상:** 주니어 개발자 + Cursor AI 협업 학습 프로젝트  
**범위:** Track A U-IN-04~05 / U-OUT-01~03 / U-FLOW-02(확장) · Track B D-LOC/MIS/VAL/SOL · G0~G3 fixture placeholder · pytest RED 확인 (Green·src/ 구현 제외)  
**선행 문서:** `Report/09-dual-track-red-design-report.md`, `Report/02-tdd-design-report.md`, `docs/PRD_MagicSquare.md`, `Report/08-test-plan-red-phase-report.md`, `.cursorrules`  
**작성일:** 2026-05-29

---

## Executive Summary

Report/09 Dual-Track RED 설계표 중 **pytest가 없던 항목**에 대해 RED Skeleton 단계 테스트 파일 10개·스켈레톤 테스트 21건을 작성했다. 각 테스트 본문은 `pytest.fail("RED: …")` 한 줄만 실행하며, Arrange/Act는 주석·production import만 허용했다. **Green 구현(`src/magicsquare/boundary/`, `entity/services/`)은 미착수**이며, 신규·기존 boundary/entity Dual-Track 테스트는 수집 단계 **ModuleNotFoundError**로 의도된 RED 상태다.

| 항목 | 결과 |
|------|------|
| **TDD phase** | RED (Skeleton) — assert·Green·Refactor 금지 |
| **Track A 스켈레톤** | 9건 (U-IN-04a/b, 05, U-OUT-01~03, U-FLOW-02 + ext×2) |
| **Track B 스켈레톤** | 12건 (D-LOC-01, D-MIS-01, D-VAL-01~06, D-SOL-01~04) |
| **Fixture placeholder** | `tests/conftest.py`, `tests/entity/conftest.py` (G0~G3 주석) |
| **Report/08 유지** | `test_ac_fr01_01_null_grid.py` 5 methods assert 불변 |
| **src/ 변경** | 없음 |
| **Green 구현** | ❌ 미착수 |

**pytest (2026-05-29 기준):**

| Suite | 결과 |
|-------|------|
| `tests/boundary/` | **5 errors** (collection — `magicsquare.boundary` 없음) |
| `tests/entity/test_d_*.py` | **4 errors** (collection — `magicsquare.entity.services` 없음) |
| `tests/entity/test_user.py` | **9 passed** (Dual-Track 범위 외 기존 Green) |
| `--continue-on-collection-errors` | **9 passed, 9 errors** |

**Transcript:** `Prompting/10-dual-track-red-skeleton-prompt.md`

---

## STEP 1 — SSOT 및 범위 확정

### 1.1 참조 문서

| SSOT | 경로 | 본 단계 사용 |
|------|------|-------------|
| RED 설계표 | `Report/09-dual-track-red-design-report.md` | Test ID, Given/Then, G0~G3 |
| TDD 계약 | `Report/02-tdd-design-report.md` | FIX-MAGIC, DT-06/10, Error code |
| PRD | `docs/PRD_MagicSquare.md` v0.2 | AC-FR01-04~06, FR-02~05 |
| Cursor Rules | `.cursorrules` | Dual-Track, pytest naming, RED 규칙 |
| 기존 RED | `Report/08-test-plan-red-phase-report.md` | UT-01 Full RED 유지 |

### 1.2 작성 범위 vs 제외

| 구분 | Test ID | 조치 |
|------|---------|------|
| **작성** | U-IN-04a/b, U-IN-05 | `test_u_in_04_*`, `test_u_in_05_*` |
| **작성** | U-OUT-01~03 | `test_u_out_output_contract.py` (03=G1 tuple passthrough 확장) |
| **작성** | U-FLOW-02 + ext | null/E004/E005 execute 0회 spy 주석 |
| **작성** | D-LOC-01 ~ D-SOL-04 | `tests/entity/test_d_*.py` 4파일 |
| **제외** | U-IN-01~03 | Report/08 Full RED — 중복 작성 금지 |
| **제외** | U-IN-06~08 | Report/09 설계표 미정의 — SSOT 추가 시 착수 |
| **불변** | Report/08 5 methods | assert 내용 수정·삭제 없음 |

---

## STEP 2 — RED Skeleton 규칙 준수

### 2.1 Skeleton 규칙 체크리스트

| # | 규칙 | 결과 |
|---|------|------|
| 1 | 테스트 구조·import·fixture placeholder만 | Pass |
| 2 | 본문 = `pytest.fail("RED: <ID> — …")` 한 줄 | Pass (21건) |
| 3 | Then assert 없음 (code/result 검증 금지) | Pass |
| 4 | skip / xfail / assert 완화 없음 | Pass |
| 5 | `src/` 프로덕션·stub 미작성 | Pass |
| 6 | GREEN / REFACTOR 미진입 | Pass |
| 7 | Domain Track Mock 금지 | Pass |
| 8 | AAA Given/When/Then = 주석만 | Pass |

### 2.2 naming · import

| 항목 | 규칙 |
|------|------|
| 함수명 | `test_<test_id>_<scenario>` (snake_case) |
| Boundary import | `magicsquare.boundary.input_validator`, `ui_boundary` |
| Entity import | `magicsquare.entity.services.*` (별칭 API) |
| U-OUT/U-FLOW | Control mock/spy — 주석만 (`SolvePartialMagicSquare.execute`) |

---

## STEP 3 — Track A: Boundary Skeleton

### 3.1 생성 파일

| 경로 | Test ID | 건수 |
|------|---------|------|
| `tests/boundary/test_u_in_04_value_range.py` | U-IN-04a, U-IN-04b | 2 |
| `tests/boundary/test_u_in_05_duplicate.py` | U-IN-05 | 1 |
| `tests/boundary/test_u_out_output_contract.py` | U-OUT-01, 02, 03 | 3 |
| `tests/boundary/test_u_flow_02_execute_isolation.py` | U-FLOW-02, ext×2 | 3 |

### 3.2 Track A Test ID ↔ Report/09

| Test ID | Then (설계) | AC / FR |
|---------|-------------|---------|
| U-IN-04a | cell=17 → E004 | AC-FR01-04 / FR-01 |
| U-IN-04b | cell=-1 → E004 | AC-FR01-04 / FR-01 |
| U-IN-05 | duplicate 5 → E005 | AC-FR01-06 / FR-01 |
| U-OUT-01 | G1 → len(result)==6, OK | FR-05 |
| U-OUT-02 | G1 → r,c ∈ [1,4] | FR-02 |
| U-OUT-03 | G1 → `[2,2,7,3,3,10]` passthrough | FR-05 (확장) |
| U-FLOW-02 | null → execute 0회 | FR-01 |
| U-FLOW-02 ext | E004/E005 → execute 0회 | FR-01 |

**Expected RED Failure:** `ModuleNotFoundError: No module named 'magicsquare.boundary'`

---

## STEP 4 — Track B: Domain Skeleton

### 4.1 생성 파일

| 경로 | Test ID | 건수 |
|------|---------|------|
| `tests/entity/test_d_loc_01.py` | D-LOC-01 | 1 |
| `tests/entity/test_d_mis_01.py` | D-MIS-01 | 1 |
| `tests/entity/test_d_val.py` | D-VAL-01~06 | 6 |
| `tests/entity/test_d_sol.py` | D-SOL-01~04 | 4 |

### 4.2 Track B Test ID ↔ Report/09

| Test ID | Given | Then (설계) | FR |
|---------|-------|-------------|-----|
| D-LOC-01 | G1 | (2,2), (3,3) row-major | FR-02 |
| D-MIS-01 | G1 | {7, 10} ascending | FR-03 |
| D-VAL-01 | G0 | true | FR-04 |
| D-VAL-02 | G0 row sum 깨짐 | false | FR-04 |
| D-VAL-03 | G0 col sum 깨짐 | false | FR-04 |
| D-VAL-04 | G0 diagonal 깨짐 | false | FR-04 |
| D-VAL-05 | 1~16 위반 | false | FR-04 |
| D-VAL-06 | 완전 격자+0 | false | FR-04 |
| D-SOL-01 | G1 | `[2,2,7,3,3,10]` | FR-05 |
| D-SOL-02 | G2 (DT-06) | `[1,1,16,4,4,1]` — **G2 TBD** | FR-05 |
| D-SOL-03 | G3 (DT-10) | UnsolvableDomainError | FR-05 |
| D-SOL-04 | G1 | len=6, 1-index | FR-05 |

**Expected RED Failure:** `ModuleNotFoundError: No module named 'magicsquare.entity.services'`

---

## STEP 5 — Fixture 부록 G0~G3

| ID | 정의 | conftest 상태 |
|----|------|---------------|
| **G0** | FIX-MAGIC (Report/02) | 주석 리터럴 |
| **G1** | blanks (2,2),(3,3); missing {7,10} | 주석 리터럴 |
| **G2** | DT-06 — (1,1)=0,(4,4)=0 | 주석 리터럴 (TBD) |
| **G3** | DT-10 unsolvable | placeholder 주석 |

경로: `tests/conftest.py` (module scope fixture 주석), `tests/entity/conftest.py` (entity re-export 주석)

---

## STEP 6 — pytest RED 검증

### 6.1 실행 명령

```powershell
python -m pytest tests/boundary/ tests/entity/ -v
python -m pytest tests/boundary/ tests/entity/ -v --continue-on-collection-errors
```

### 6.2 결과 요약

| 구분 | 파일 수 | collection | pytest.fail 실행 |
|------|---------|------------|------------------|
| boundary (기존 UT-01) | 1 | ERROR | — (import 단계) |
| boundary (신규) | 4 | ERROR | Green 후 FAIL→PASS |
| entity (신규 D-*) | 4 | ERROR | Green 후 FAIL→PASS |
| entity (User) | 1 | OK | 9 passed |

기본 `-v` 실행 시 수집 중단 → **passed 0** (User 테스트 미실행).  
`--continue-on-collection-errors` 시 Dual-Track 9 errors + User 9 passed.

---

## STEP 7 — RED Skeleton 검수

| # | 항목 | 결과 |
|---|------|------|
| 1 | Report/09 미작성 Test ID 스켈레톤화 | Pass (21건) |
| 2 | Report/08 assert 불변 | Pass |
| 3 | src/ 무변경 | Pass |
| 4 | skip/xfail/assert Then 없음 | Pass |
| 5 | Domain Mock 없음 | Pass |
| 6 | D-SOL-02 G2 TBD 표시 | Pass |
| 7 | U-IN-01~03 중복 없음 | Pass |

---

## Traceability (FR → Skeleton Test ID)

| FR | Track A (신규) | Track B (신규) |
|----|----------------|----------------|
| FR-01 | U-IN-04a/b, 05, U-FLOW-02 | — |
| FR-02 | U-OUT-02 | D-LOC-01 |
| FR-03 | — | D-MIS-01 |
| FR-04 | — | D-VAL-01~06 |
| FR-05 | U-OUT-01, 02, 03 | D-SOL-01~04 |

---

## 교차 이슈

| ID | 이슈 | 권장 |
|----|------|------|
| X-01 | U-IN-06~08 요청 vs Report/09 미정의 | SSOT 통일 후 스켈레톤 추가 |
| X-02 | U-OUT-03 Report/09 미포함 | v0.2 확장으로 기록; Green 전 설계표 반영 검토 |
| X-03 | collection ERROR vs pytest.fail | Green 전 import 성공 시 fail 메시지로 RED 유지 가능 |
| X-04 | test_user.py 9 passed | Dual-Track 범위 외; 전체 passed 0 목표와 분리 해석 |
| X-05 | G1 vs DT-03 격자 불일치 (Report/09 X-02) | Green 전 G1 리터럴 SSOT 확정 |

---

## 다음 단계 (권장)

- [ ] **DEF-001 Green:** `magicsquare.boundary` 최소 모듈 — U-IN-04a 1건 PASS
- [ ] **DEF-002·003:** Report/08 UT-01 ↔ PRD SSOT 정렬
- [ ] U-IN-02~03 Skeleton (Report/08 P1) — Full RED assert 버전
- [ ] `magicsquare.entity.services` — D-VAL-01 Green (DT-01 병행)
- [ ] G1/G2 리터럴 SSOT 확정 (Report/09 X-02)
- [ ] Skeleton → Full RED: 주석 Arrange/Act 연결 + Then assert (1 TC-ID = 1 cycle)

---

## 변경 이력

| 날짜 | 내용 |
|------|------|
| 2026-05-29 | Report/09 기반 Dual-Track RED Skeleton 21건 · conftest placeholder → Report/10 · Prompting/10 Export |

---

## 부록 A — 생성·갱신 파일

| 경로 | 설명 |
|------|------|
| `tests/conftest.py` | G0~G3 fixture placeholder (주석) |
| `tests/entity/conftest.py` | Entity fixture placeholder |
| `tests/boundary/test_u_in_04_value_range.py` | U-IN-04a/b |
| `tests/boundary/test_u_in_05_duplicate.py` | U-IN-05 |
| `tests/boundary/test_u_out_output_contract.py` | U-OUT-01~03 |
| `tests/boundary/test_u_flow_02_execute_isolation.py` | U-FLOW-02 + ext |
| `tests/entity/test_d_loc_01.py` | D-LOC-01 |
| `tests/entity/test_d_mis_01.py` | D-MIS-01 |
| `tests/entity/test_d_val.py` | D-VAL-01~06 |
| `tests/entity/test_d_sol.py` | D-SOL-01~04 |
| `Report/10-dual-track-red-skeleton-report.md` | 본 보고서 |
| `Prompting/10-dual-track-red-skeleton-prompt.md` | Transcript Export |
| `README.md` | Report/10, Prompting/10, 진행 상황 갱신 |

## 부록 B — 관련 문서

| 문서 | 경로 |
|------|------|
| RED 설계표 | `Report/09-dual-track-red-design-report.md` |
| 테스트 플랜·RED QA | `Report/08-test-plan-red-phase-report.md` |
| TDD 설계 SSOT | `Report/02-tdd-design-report.md` |
| 결함 목록 | `defect_list.md` |
