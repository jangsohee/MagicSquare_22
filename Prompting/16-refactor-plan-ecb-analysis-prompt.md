# Magic Square — REFACTOR 계획 · ECB 분석 (transcript)
_Exported on 2026-05-29 from Cursor — Green/Golden Master 이후 Refactor 사전 분석 → Report/16 Export_  
_선행: `Report/14`, `Report/15`, `Report/02`, `.cursorrules`, `README.md`_

---

**User**

리팩토링 대상:
- `src/control/solve_partial_magic_square.py`
- `src/boundary/ui_boundary.py`
- `src/boundary/screen/main_window.py`

1. 각 파일에 대응하는 test_*.py가 있는지, 없으면 어떤 테스트가 필요한지
2. 현재 RED 스켈레톤(pytest.fail) 중 리팩토링 전 GREEN으로 만들어야 할 것
3. 테스트 없이 리팩토링을 시작하면 안 되는 이유 (한 줄)

REFACTOR phase 기준(.cursorrules)으로 답해줘.

---

**Cursor**

실경로: `src/magicsquare/...` · Screen = `boundary/gui/main_window.py`

**pytest:** 60 passed · `pytest.fail` RED skeleton **0건**

| 파일 | 1:1 test | 간접 커버 | Refactor 전 필요 |
|------|----------|-----------|------------------|
| `solve_partial_magic_square.py` | 없음 | IT-OK/FAIL, GM, entry | `tests/control/test_solve_partial_execute.py` |
| `ui_boundary.py` | 없음 | U-FLOW-02, IT-*, GM | `tests/boundary/test_ui_boundary.py` |
| `main_window.py` | 없음 | — | `tests/boundary/gui/test_main_window.py` |

**RED→Green 잔존:** 없음 (Report/10 skeleton → Green 완료). **main_window는 테스트 자체 없음.**

**한 줄:** Refactor phase는 전체 Green + pytest PASS 전제 — 테스트 없이 구조 변경 시 observable behavior 회귀 검출 불가.

---

**User**

ECB 매핑 (domain/boundary/gui → 실제 파일). 연관: `input_validator`, `two_cell_solver`, `.cursorrules`

1. 각 파일 ECB 역할 현황 (표)
2. 잘못된 위치 코드 — 이동 대상
3. Control vs Entity 혼재 (`two_cell_solver` 경계)
4. REFACTOR phase 한 줄 결론 + P0/P1 (Step 1·2 연계)

코드 수정안·패치 금지.

---

**Cursor**

**역할 현황**

| 파일 | 역할 | 적합 |
|------|------|------|
| `solve_partial_magic_square.py` | Control | 부분 — envelope 조립이 Boundary 침범 |
| `ui_boundary.py` | Boundary | 부분 — E006/E007·facade SSOT 미완 |
| `main_window.py` | Screen | 부분 — GUI 테스트 0% · except Exception |

**이동 대상**

- Control 5–37행 envelope → `boundary/response_mapper.py`
- `entry`/`ui_boundary` facade 통합
- `EXAMPLE_GRID` → `tests/conftest.py`
- null E001 → Report/02 `ERR_NULL_GRID` (DEF-002)

**Entity:** `two_cell_solver` 적합 · Control과 중복 없음 · Entity 분리 불필요

**P0:** Control envelope 제거 · facade/E001 · GUI 테스트  
**P1:** fixture · presenter · DRY · MagicConstant SSOT

---

**User**

점검: 함수 다중 역할 · 클래스 데이터+검증 혼재 · UI 비즈니스 판단  
위반만 `파일:줄번호` 형식. 코드 수정안 금지.

---

**Cursor**

**① 함수 다중 역할**

| 파일:줄 | 역할 1 | 역할 2 |
|---------|--------|--------|
| `solve_partial_magic_square.py:18-37` | Domain 오케스트레이션 | envelope 조립 |
| `ui_boundary.py:20-35` | E001~E005 검증 | Control 위임 |
| `main_window.py:39-47` | UI 구성 | fixture 주입 |
| `main_window.py:95-101` | 데이터 주입 | UI 상태 갱신 |
| `main_window.py:111-126` | 입력·호출 | 예외 폴백·라우팅 |

**② 클래스 데이터+검증:** 해당 없음 (MainWindow UI 복수 책임 별도 표기)

**③ UI 비즈니스 판단:** 해당 없음

---

**User**

앞서 분석 바탕 리팩토링 계획서 작성. 코드 수정 금지.

- 리팩토링 대상 목록 (우선순위)
- 테스트 선행 필요 항목
- 리팩토링 후 검증 방법

---

**Cursor**

12건 대상 P0~P2 표 · P0 테스트 5종 · pytest/GM/offscreen smoke 검증 �手順 정리.

**1순위:** Control envelope → Boundary · facade/E001 통합 · GUI 테스트 게이트. Entity(`two_cell_solver`) 제외.

---

**User**

Report 폴더에 보고서 생성하고, Prompting 폴더에 Transcript도 Export 해줘. readme 파일도 업데이트해주고

---

**Cursor**

**산출물:**

| 유형 | 경로 |
|------|------|
| 보고서 | `Report/16-refactor-plan-ecb-analysis-report.md` |
| Transcript | `Prompting/16-refactor-plan-ecb-analysis-prompt.md` |

**README 갱신:**
- 현재 단계 — REFACTOR 계획 수립 (Green 13/13 · GM 60 passed)
- 문서 링크 Report/16 · Prompting/16
- REFACTOR To-Do · pytest 60 · 미해결 DEF-002/003 Refactor 연계

---

## Export 메타

| Field | Value |
|-------|-------|
| Report | `Report/16-refactor-plan-ecb-analysis-report.md` |
| Transcript | `Prompting/16-refactor-plan-ecb-analysis-prompt.md` |
| TDD phase | REFACTOR planning (구현 미착수) |
| pytest | 60 passed |
| Next | P0 테스트 Green → Control envelope 분리 → facade 통합 |
