# Magic Square 프로젝트 — Cursor Rules 및 1차 구현 보고서

**작성 목적:** Cursor AI 협업 규칙 고정 및 Python ECB 1차 구현(User 엔티티) 결과 정리  
**대상:** 주니어 개발자 + Cursor AI 활용 학습 프로젝트  
**범위:** `.cursorrules` · `.cursor/rules/*.mdc` · `pyproject.toml` · entity 레이어 User · pytest  
**선행 문서:** `Report/01-problem-definition-report.md`, `Report/02-tdd-design-report.md`  
**작성일:** 2026-05-28  
**현행 규칙:** `.cursor/rules/magicsquare-*.mdc` 5파일 — [`Report/04`](04-magicsquare-rules-consolidation-report.md) 참조  
> 본 문서는 **11개 번호 규칙(`00~42`) 생성·User Entity** 시점 기록이다. 이후 5파일로 통합되었으며 상세는 Report/04에 있다.

---

## Executive Summary

본 단계에서 MagicSquare 프로젝트는 **설계 문서(Report/02) 이후** Cursor Rules 체계를 구축하고, Python **ECB 패턴**으로 첫 도메인 코드(`User` 엔티티)를 추가했다.

| 산출물 | 상태 |
|--------|------|
| `.cursorrules` (YAML 8섹션) | 완료 |
| `.cursor/rules/*.mdc` (11개, **이후 Report/04에서 5개로 통합**) | 완료 → 통합됨 |
| `pyproject.toml` | 완료 |
| `src/magicsquare/entity/` (User) | 완료 |
| `tests/entity/test_user.py` | 9 tests PASS |
| 마방진 핵심 로직 (DT-01~) | 미착수 |

**주의:** Report/02의 레이어 명칭(Logic/Screen/Domain)과 `.cursorrules`의 ECB 매핑(boundary/control/entity) 및 `.mdc` 일부 내용이 **완전히 동기화되지 않음**. 마방진 본 구현 전 harmonization 필요.

---

## STEP 1 — Cursor Rules 설계 결정

### 1.1 `.cursorrules` vs `.cursor/rules/*.mdc`

| 방식 | 채택 | 이유 |
|------|------|------|
| `.cursor/rules/*.mdc` | **권장·생성함** | glob별 레이어 규칙, Dual-Track 분리, Rule picker |
| `.cursorrules` (YAML) | **보조 요약** | 프로젝트 전역 개요·8섹션 단일 참조 |

### 1.2 `.mdc` 파일 목록 (11개, 당시 — 현재는 Report/04의 5파일)

| 파일 | alwaysApply | glob | 역할 |
|------|-------------|------|------|
| `00-project-guardrails.mdc` | true | — | RED 우선, 테스트 약화·print() 금지 |
| `01-io-contract.mdc` | true | — | 입출력 계약, Magic Constant=34 |
| `10-python-style.mdc` | false | `**/*.py` | PEP8, type hints |
| `20-ecb-architecture.mdc` | false | `src/**/*.py` | ECB 의존 방향 |
| `30-entity-domain.mdc` | false | `entity/**` | Domain 순수 로직 |
| `31-boundary-screen.mdc` | false | `boundary/**` | I/O 검증 |
| `32-control-usecase.mdc` | false | `control/**` | Use case |
| `33-data-repository.mdc` | false | `data/**` | Repository |
| `40-pytest-aaa.mdc` | false | `tests/**` | AAA |
| `41-tdd-dual-track.mdc` | false | `tests/**` | Dual-Track 순서 |
| `42-integration-tests.mdc` | false | `integration/**` | IT 시나리오 |

---

## STEP 2 — `.cursorrules` YAML 구조

### 2.1 최상위 8키

`project` · `code_style` · `architecture` · `tdd_rules` · `testing` · `forbidden` · `file_structure` · `ai_behavior`

각 키 앞 **80자 `#` 구분선** 주석.

### 2.2 `tdd_rules` 세분화 (Red / Green / Refactor)

| Phase | description | 핵심 must_not |
|-------|-------------|---------------|
| **red_phase** | 실패 테스트 먼저, pytest FAIL 확인 | src/ 선행 추가, skip/xfail |
| **green_phase** | 최소 구현으로 1개 PASS | 리팩터링, assert 약화 |
| **refactor_phase** | behavior 불변 구조 개선 | observable 변경, 테스트 약화 |

### 2.3 `.cursorrules` 검토에서 발견된 문제 (수정 전 상태 기록)

| # | 유형 | 내용 |
|---|------|------|
| 1 | 충돌 | `skip/xfail`: forbidden 무조건 vs tdd_rules 조건부 표현 |
| 2 | 충돌 | refactor 시 prod 변경 vs forbidden "RED 없이 구현" (문자 그대로) |
| 3 | 운영 | coverage gate·pytest 실행 — 도구 미구성 시 AI가 검증 불가 |
| 4 | 형식 | Cursor가 YAML 트리로 enforce하지 않을 수 있음 → `.mdc`가 실효적 |

> 이후 `.cursorrules` 전체 섹션 채우기 작업에서 `forbidden`을 pattern/reason/alternative 구조로 확장하고, refactor는 "observable behavior 변경 금지"로 명시해 **B항 부분 완화**.

---

## STEP 3 — Python 프로젝트 기반 구조

### 3.1 `pyproject.toml`

- `requires-python >= 3.10`
- `[tool.pytest.ini_options] pythonpath = ["src"]`, `testpaths = ["tests"]`
- black / ruff line-length 88

### 3.2 디렉터리 (신규)

```
src/magicsquare/
├── __init__.py
└── entity/
    ├── __init__.py
    ├── errors.py
    └── user.py
tests/entity/
└── test_user.py
```

---

## STEP 4 — User 엔티티 (ECB entity 레이어)

### 4.1 목적

- Data layer session key(`user_id`) 및 boundary 표시명(`display_name`)의 **도메인 불변식** 고정
- I/O·UI message 없음 (ECB entity 책임)

### 4.2 도메인 모델

| 타입 | 설명 |
|------|------|
| `User` | frozen dataclass, `user_id`, `display_name` |
| `UserValidationError` | `code` + message, entity 전용 |
| `USER_ID_MAX_LENGTH` | 64 |
| `DISPLAY_NAME_MAX_LENGTH` | 100 |

### 4.3 Invariant

1. `user_id` — strip 후 non-empty, 길이 ≤ 64  
2. `display_name` — strip 후 non-empty, 길이 ≤ 100  
3. 인스턴스 **불변** (`frozen=True`, `slots=True`)

### 4.4 Public API

- `User.create(user_id: str, display_name: str) -> User`
- 실패 시 `UserValidationError` (`INVALID_USER_ID` / `INVALID_DISPLAY_NAME`)

### 4.5 [TDD WARNING]

`.cursorrules`는 **Red → Green** 순서를 요구하나, User 구현은 **테스트·코드 동시 작성** 요청으로 진행됨. 이후 마방진 핵심(DT-01~)부터 Red 선행 권장.

---

## STEP 5 — 테스트 결과

**파일:** `tests/entity/test_user.py`  
**패턴:** pytest + AAA  
**결과:** **9 passed** (2026-05-28 실행)

| 테스트 클래스 | 케이스 수 | 검증 대상 |
|---------------|-----------|-----------|
| `TestUserCreate` | 3 | 정상 생성, 불변성, 동등성 |
| `TestUserIdValidation` | 3 | empty, whitespace, max length |
| `TestDisplayNameValidation` | 3 | empty, whitespace, max length |

---

## STEP 6 — 레이어 매핑 불일치 (기술 부채)

| 문서 | entity | control | boundary |
|------|--------|---------|----------|
| **Report/02** | Logic/Domain (MagicSquareJudge 등) | Application (선택) | Screen/I/O |
| **.cursorrules (최신)** | 도메인 데이터·규칙 | **비즈니스 로직** | 외부 I/O |
| **`.mdc` (30-entity)** | MagicSquareJudge 등 (Report/02 기준) | — | — |

**권장 다음 작업:** Report/03 부록 harmonization 표 작성 후 `.mdc` 또는 Report/02 중 하나를 단일 기준으로 확정.

---

## 미해결 항목

- [ ] Report/02 ↔ `.cursorrules` ECB 레이어 정의 harmonization
- [ ] `.cursorrules` control/entity 역할과 Report/02·`magicsquare-ecb-architecture.mdc` 동기화
- [ ] Mom Test · 1차 사용자 확정
- [ ] DT-01 (`MagicSquareJudge`) Red 테스트부터 마방진 핵심 구현
- [ ] boundary / control / data 레이어 구현
- [ ] `pytest-cov` CI 및 커버리지 gate

---

## 다음 단계 (권장 순서)

1. ECB 레이어 정의 단일화 (문서 1회 정렬)
2. `tests/control/test_dt01_*.py` Red → `MagicSquareJudge` Green
3. boundary validator (UT-01~) 병행
4. User ↔ data `MatrixRepository` session id 연동

---

## 부록 A — 생성·갱신 파일 목록

| 경로 | 설명 |
|------|------|
| `.cursorrules` | YAML 8섹션 전역 규칙 |
| `.cursor/rules/*.mdc` | 11개 레이어별 규칙 (**삭제됨** → Report/04의 `magicsquare-*.mdc` 5개) |
| `pyproject.toml` | pytest/pythonpath |
| `src/magicsquare/entity/user.py` | User 엔티티 |
| `src/magicsquare/entity/errors.py` | UserValidationError |
| `tests/entity/test_user.py` | entity 테스트 |

---

## 부록 B — 관련 프롬프팅

| 문서 | 설명 |
|------|------|
| `Prompting/03-cursor-rules-implementation-prompt.md` | 본 단계 Cursor 대화 Transcript Export |
| `Report/04-magicsquare-rules-consolidation-report.md` | Rules 11→5 통합 (현행 구조) |
| `Prompting/04-magicsquare-rules-consolidation-prompt.md` | 통합 단계 Transcript |
