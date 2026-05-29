# Magic Square — Golden Master 회귀 안전장치 (transcript)
_Exported on 2026-05-29 from Cursor — GM baseline → approve tests → README To-Do → Report/15 Export_  
_선행: `Report/02`, `Report/14`, `README.md`, Green 13/13 완료_

---

**User**

[P] 회귀 테스트(Approval/Golden Master) 설계 전문가입니다.  
[C] pytest/XUnit/Catch2 기반 테스트 환경  
[T] Magic Square Solver 출력 기반 Golden Master 기준 파일을 생성해줘.

구현 요구사항:
1. 기준 출력 파일 생성 전략 — 정상/reverse/invalid blank/duplicate/no solution
2. approve 패턴 — 파일 없으면 생성, 있으면 비교, 불일치 시 unified diff FAIL
3. 기준 파일 구조 `[normal_success]` Input/Output 섹션

[F] `tests/golden_master_expected.txt` + 생성 스크립트 + approve 패턴 설계 문서

---

**Cursor**

코드베이스 탐색 — Solver는 stdout이 아닌 `UIBoundary.solve()` TypedDict envelope 반환.

**실제 Solver 출력 (5 시나리오):**

| Scenario | Output |
|----------|--------|
| normal_success | `[3,3,6,4,4,1]` |
| reverse_success | `[1,1,16,4,4,1]` |
| invalid_blank_count | `ERR_EMPTY_COUNT` |
| duplicate_number | `ERR_DUPLICATE` |
| no_valid_solution | `ERR_NO_SOLUTION` |

> 예시 `[3,3,1,4,4,6]`과 달리 GM-TC-01 grid는 forward 실패·reverse만 성공.

**산출물:**

| 파일 | 역할 |
|------|------|
| `tests/golden_master_expected.txt` | baseline |
| `scripts/generate_golden_master.py` | 재생성 스크립트 |
| `tests/golden_master/approval.py` | approve 패턴 |
| `tests/golden_master/format.py` | serialize/parse |
| `tests/golden_master/scenarios.py` | 입력 grids |
| `tests/golden_master/builder.py` | live solver runner |
| `docs/golden_master_approval_design.md` | 설계 문서 |

`git add tests/golden_master_expected.txt` 실행.

---

**User**

[P] 회귀 테스트(Approval/Golden Master) 설계 전문가  
[T] Magic Square Solver Golden Master **테스트 코드** 작성

구현 요구사항:
1. API result serialization
2. `open(expected).read() vs actual` approve 패턴
3. `@pytest.mark.golden_master` / `[TAG][GoldenMaster]`
4. `pytest -m golden_master -v`
5. 실패 시 `--- expected` / `+++ actual` diff

테스트 케이스: GM-TC-01~05 (정상/reverse/INVALID_BLANK_COUNT/DUPLICATE/NO_VALID_MAGIC_SQUARE)

검증: int[6], row-major, 1-index, small-first+reverse fallback, Error Contract

[F] `test_golden_master_magic_square.*` + `golden_master_expected.txt` + 실행 결과 예시

---

**Cursor**

GM-TC-01~05 개별 테스트 + contract validators 구현.

**주요 파일:**

- `tests/integration/test_golden_master_magic_square.py` — 6 tests (TC-01~05 + full baseline)
- `tests/golden_master/validators.py` — int[6], row-major, assignment, error contract
- `tests/golden_master/approval.py` — `approve_section`, diff headers `expected`/`actual`
- `tests/conftest.py` — `golden_master_update` fixture, marker 등록
- `pyproject.toml` — `markers = ["golden_master: ..."]`

**실행 결과:**

```text
$ pytest -m golden_master -v
collected 60 items / 54 deselected / 6 selected
test_gm_tc_01_normal_success PASSED
test_gm_tc_02_reverse_success PASSED
test_gm_tc_03_invalid_blank_count PASSED
test_gm_tc_04_duplicate_number PASSED
test_gm_tc_05_no_valid_magic_square PASSED
test_gm_tc_all_sections_match_full_baseline PASSED
6 passed, 54 deselected in 0.12s
```

**실패 diff 예시:**

```text
--- expected
+++ actual
@@ -5,4 +5,4 @@
 Output:
-[3,3,6,4,4,1]
+[9,9,9,9,9,9]
```

---

**User**

README 파일에 `## RED 단계 To-Do 리스트` 아래 Golden Master 회귀 안전장치 섹션 추가.

GM-01~GM-10:
- 기준 파일 생성 (GM-01~03)
- 테스트 코드 (GM-04~06)
- 회귀 보호 (GM-07~10)

---

**Cursor**

`README.md` (루트) `## RED 단계 To-Do 리스트` 직하에 섹션 삽입.

- ### Golden Master 회귀 안전장치
- > Refactoring 시작 전 구축. GREEN 완료 후 즉시 적용.
- GM-01~GM-10 전부 `[x]` (구현 완료)

---

**User**

Report 폴더에 보고서 생성하고, Prompting 폴더에 Transcript도 Export 해줘

---

**Cursor**

**pytest 재확인 (2026-05-29):**

```
pytest -m golden_master -v → 6 passed, 54 deselected
pytest tests/ -q → 60 passed
```

**산출물:**

| 유형 | 경로 |
|------|------|
| 보고서 | `Report/15-golden-master-regression-report.md` |
| Transcript | `Prompting/15-golden-master-regression-prompt.md` |

**README** 문서 링크 테이블에 Report/15 · Prompting/15 추가.

---

## Export 메타

| Field | Value |
|-------|-------|
| Report | `Report/15-golden-master-regression-report.md` |
| Transcript | `Prompting/15-golden-master-regression-prompt.md` |
| TDD phase | GREEN 완료 → REFACTOR 전 GM 구축 |
| GM checklist | GM-01~GM-10 ✅ |
| Golden Master tests | 6 passed (`pytest -m golden_master -v`) |
| Full suite | 60 passed |
| Baseline | `tests/golden_master_expected.txt` |
| Next | REFACTOR + CI golden_master gate (선택) |
