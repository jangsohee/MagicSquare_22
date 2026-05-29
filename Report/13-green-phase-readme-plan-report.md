# Magic Square 프로젝트 — GREEN 단계 README·묶음 계획 보고서

**작성 목적:** A-01 Green 이후 **RED/Green 묶음 전략** 확정 · README GREEN To-Do 체크리스트 반영 · pytest 현황 갱신  
**대상:** 주니어 개발자 + Cursor AI 협업 학습 프로젝트  
**범위:** Track A/B/I 13 Green 묶음 · RED 1묶음=GREEN 1커밋 · README·pytest 현황 · DEF-001 부분 해소  
**선행 문서:** `Report/12-ac-fr01-01-green-phase-report.md`, `Report/10-dual-track-red-skeleton-report.md`, `defect_list.md`, `README.md`  
**작성일:** 2026-05-29

---

## Executive Summary

UT-01 Green(A-01) 완료 이후, RED/Green을 **커밋 묶음 단위**로 정렬하는 계획을 확정하고 README에 **GREEN 단계 To-Do 리스트**를 추가·갱신했다. TDD 사이클(Red 1→Green 1)과 git 커밋 묶음을 분리하여, **같은 코드 분기/AC = RED 1커밋 ↔ GREEN 1커밋** 원칙을 적용했다.

| 항목 | 결과 |
|------|------|
| **TDD phase** | GREEN 진행 중 (A-01 완료 / 12 remaining) |
| **Green 묶음** | Track A 8 · Track B 3 · Integration 2 = **13** |
| **완료** | A-01 (UT-01 null, 5 passed) |
| **다음 착수** | A-02 (UT-02 rows) 또는 B-01 (D-VAL) 병렬 |
| **README** | pytest 현황 · RED/GREEN To-Do · Report/13 링크 |
| **DEF-001** | **부분 해소** — boundary 패키지·UT-01 PASS |

**pytest (2026-05-29 기준):**

| Suite | 결과 |
|-------|------|
| `test_ac_fr01_01_null_grid.py` | **5 passed** |
| `tests/boundary/` | **5 passed, 3 failed, 2 errors** |
| `tests/entity/test_user.py` | **9 passed** |
| `tests/entity/test_d_*.py` | **4 errors** (collection) |

**Transcript:** `Prompting/13-green-phase-readme-plan-prompt.md`

---

## STEP 1 — RED/Green 묶음 원칙 확정

### 1.1 두 축 분리

| 축 | 단위 | 용도 |
|----|------|------|
| **TDD 사이클** | Red 1 test → Green 1 test | 로컬 구현 (`.cursorrules` green_phase) |
| **Git 커밋 묶음** | Red N tests 1커밋 ↔ Green 1커밋 | 버전 관리·리뷰 |

### 1.2 묶음 기준

- **같은 `if` 분기** 또는 **같은 AC** → RED 1묶음 = GREEN 1묶음
- Domain Track B는 A-01 이후 **병렬** 가능
- U-FLOW null 격리는 **A-01에 포함** — A-07은 E004/E005만
- U-OUT + UT-09 성공 경로는 **A-08**으로 통합

### 1.3 점검에서 수정한 항목

| 이슈 | 조치 |
|------|------|
| Green을 test 1건=1커밋으로 과도 분해 | 커밋 묶음 기준으로 재정렬 |
| R-07 null vs A-01 중복 | A-07에서 null 제외 |
| R-11 vs R-12 성공 경로 중복 | A-08로 통합 |

---

## STEP 2 — Green 묶음 카탈로그 (13)

### 2.1 Track A — Boundary (순차)

| 묶음 | TC | AC/FR | Green 구현 | RED 상태 | Green 상태 |
|------|-----|-------|------------|----------|------------|
| **A-01** | UT-01 ×5 | AC-FR01-01 | `grid is None` → ERROR | Full RED ✅ | **Green ✅** |
| **A-02** | UT-02 ×3 | AC-FR01-02 | `ERR_GRID_ROWS` | 미작성 | |
| **A-03** | UT-03 ×2 | AC-FR01-03 | `ERR_GRID_COLS` | 미작성 | |
| **A-04** | UT-04/05 ×2 | AC-FR01-04 | `ERR_VALUE_RANGE` | Skeleton | |
| **A-05** | UT-06/07 ×2 | AC-FR01-05 | `ERR_EMPTY_COUNT` | 미작성 | |
| **A-06** | UT-08 ×1 | AC-FR01-06 | `ERR_DUPLICATE` | Skeleton | |
| **A-07** | U-FLOW ×2 | FR-01 | execute 0회 (E004/E005) | Skeleton | |
| **A-08** | UT-09+U-OUT ×4 | AC-FR01-07 | OK envelope + passthrough | Skeleton | |

### 2.2 Track B — Domain (병렬)

| 묶음 | TC | FR | Green 구현 | RED 상태 |
|------|-----|-----|------------|----------|
| **B-01** | D-VAL ×6 | FR-04 | `is_magic_square()` | Skeleton |
| **B-02** | D-LOC + D-MIS ×2 | FR-02/03 | blank + missing | Skeleton |
| **B-03** | D-SOL ×4 | FR-05 | `solution()` | Skeleton |

### 2.3 Integration

| 묶음 | TC | Green 구현 | 선행 |
|------|-----|------------|------|
| **I-01** | IT-FAIL ×3~5 | invalid E2E, Mock 금지 | A-01~06 |
| **I-02** | IT-OK ×3 | solve E2E + save/load | A-08, B-03 |

---

## STEP 3 — README 갱신 내용

### 3.1 추가·수정 섹션

| 섹션 | 변경 |
|------|------|
| 상단 현재 단계 | GREEN A-01 완료 · Report/13 링크 |
| **pytest 현황** | 신규 — suite별 pass/fail/error 표 |
| 진행 상황 | A-01 Green · Report/13 · A-02~ / B-01 착수 항목 |
| RED To-Do | UT-01 RED 완료 체크 · Skeleton P2 항목 정리 · DEF-002 drift 명시 |
| GREEN To-Do | 13묶음 체크리스트 (A-01 ✅) |
| 미해결 항목 | DEF-001 부분 해소 · DEF-002·003 drift |
| 로컬 실행 | A-01·boundary·continue-on-collection-errors 명령 |
| 프로젝트 구조 | boundary 4파일 · Report/13 · Prompting/13 |

### 3.2 README GREEN To-Do 구조

각 묶음 4항목:

1. RED (파일·건수)
2. GREEN (최소 구현)
3. pytest 명령
4. 커밋 메시지 예

---

## STEP 4 — 결함·계약 상태

| ID | Before | After (A-01) |
|----|--------|--------------|
| **DEF-001** | boundary 없음 → 수집 ERROR | **부분 해소** — UT-01 PASS. U-OUT/U-FLOW `ui_boundary` ERROR 잔존 |
| **DEF-002** | Open | Open — 테스트 `INVALID_SIZE` vs PRD `ERR_NULL_GRID` |
| **DEF-003** | Open | Open — `@patch resolve` vs `solve_partial_grid` |
| **DEF-004** | Open | Open — `test_d_*` 수집 ERROR |

---

## STEP 5 — Green 진행 흐름

```
Track A (순차)          Track B (병렬)
A-01 NULL ✅            B-01 D-VAL
A-02 ROWS               B-02 LOC/MIS
A-03 COLS               B-03 SOL
A-04 RANGE                    │
A-05 EMPTY                    │
A-06 DUPLICATE                │
A-07 FLOW ────────────────────┤
A-08 SUCCESS ◄────────────────┘
         │
         ▼
      I-01 IT-FAIL → I-02 IT-OK
```

---

## STEP 6 — Green 마일스톤

| 마일스톤 | 완료 조건 |
|----------|-----------|
| FR-01 입력 검증 Green | A-01~A-06 |
| Domain Core Green | B-01~B-03 |
| 성공 경로 Green | A-08 |
| Integration Green | I-01~I-02 |
| Boundary cov 85%+ | A-01~A-08 |
| Domain cov 95%+ | B-01~B-03 |

---

## References

| 문서 | 용도 |
|------|------|
| `Report/12-ac-fr01-01-green-phase-report.md` | A-01 Green 구현 |
| `Report/02-tdd-design-report.md` | 검증 순서 · TC-ID SSOT |
| `Report/10-dual-track-red-skeleton-report.md` | Skeleton 21건 |
| `README.md` | GREEN To-Do · pytest 현황 |
| `defect_list.md` | DEF-001~006 |
