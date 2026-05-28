# Magic Square 프로젝트 — Cursor Rules 통합(5파일) 보고서

**작성 목적:** `00~42` 번호 규칙 11개를 실습용 `magicsquare-*.mdc` 5파일 구조로 통합한 결과 정리  
**대상:** 주니어 개발자 + Cursor AI 협업 학습 프로젝트  
**범위:** `.cursor/rules/` 재구성 · `.cursorrules` 참조 갱신 · 구조 비교·결정 기록  
**선행 문서:** `Report/03-cursor-rules-and-implementation-report.md`  
**작성일:** 2026-05-28

---

## Executive Summary

직전 세션에서 **Cursor Rules 확장 실습**(예: `D:\...\MagicSquare_개선`의 5파일 구조)을 진행했다. 구조 비교 후 사용자 요청에 따라 **주제별 5파일(`magicsquare-*.mdc`)** 로 통합하고, 중복을 피하기 위해 기존 **번호 규칙 11개를 삭제**했다.

| 산출물 | 이전 (Report/03) | 현재 (본 단계) |
|--------|------------------|----------------|
| `.cursor/rules/*.mdc` | 11개 (`00~42`) | **5개** (`magicsquare-*`) |
| `.cursorrules` references | `*.mdc` 와일드카드 | 5파일 **명시 목록** |
| `src/` · `tests/` | User Entity, 9 tests | **변경 없음** |
| 마방진 핵심 (DT-01~) | 미착수 | 미착수 |

**pytest:** `9 passed` (2026-05-28, `tests/entity/test_user.py`)

---

## STEP 1 — 실습 배경

### 1.1 요청 맥락

다음과 같은 **5파일 확장 실습** 구조를 참고해 진행 방법을 문의했다.

```
.cursorrules
.cursor/rules/
    magicsquare-ecb-architecture.mdc
    magicsquare-forbidden.mdc
    magicsquare-project.mdc
    magicsquare-python-code-style.mdc
    magicsquare-tdd-testing.mdc
```

### 1.2 프로젝트 당시 상태 (Report/03 이후)

- `.cursorrules` — YAML 8섹션 완성
- `.cursor/rules/` — `00-project-guardrails` ~ `42-integration-tests` **11개**
- `src/magicsquare/entity/` — `User` 엔티티
- `tests/entity/test_user.py` — 9 tests PASS

---

## STEP 2 — 구조 비교 및 권장안

### 2.1 비교 요약

| 기준 | `magicsquare-*` 5파일 | `00~42` 11파일 |
|------|----------------------|----------------|
| 학습·실습 | 주제 5개로 이해 쉬움 | 파일 수 많아 보일 수 있음 |
| 실제 코딩 | 레이어/트랙별 정밀도 낮음 | **작업 중인 경로에 맞는 규칙만** (`globs`) |
| ECB·TDD 훈련 | 한 덩어리로 묶임 | entity/boundary/control/data·AAA/IT **분리** |
| 토큰·노이즈 | `alwaysApply` 과다 시 부담 | 대부분 24~33줄, glob 조건부 적용 |

### 2.2 AI 권장 (결정 전)

- **마방진 TDD 본 구현 단계:** 11파일 세분화 + `.cursorrules` 짧은 인덱스가 **운영상 유리**
- **규칙 문법·frontmatter 입문 실습:** 5파일 구조가 **교재용으로 적합**
- **둘 다 유지:** 내용 중복 → AI 혼동 **비추천**

### 2.3 사용자 결정

> `./cursor/rules/*.mdc` 형식으로 만들어줘

→ **5파일 통합** 채택. 기존 11개는 **삭제**(복사 2벌 유지하지 않음).

---

## STEP 3 — 통합 매핑 (11 → 5)

| 신규 파일 | `alwaysApply` / `globs` | 통합 원본 |
|-----------|-------------------------|-----------|
| `magicsquare-project.mdc` | `true` | `00-project-guardrails` + `01-io-contract` |
| `magicsquare-forbidden.mdc` | `true` | `.cursorrules` `forbidden` + guardrails 금지 항목 |
| `magicsquare-ecb-architecture.mdc` | `src/**/*.py` | `20-ecb-architecture` + `30~33` (entity/boundary/control/data) |
| `magicsquare-python-code-style.mdc` | `**/*.py` | `10-python-style` |
| `magicsquare-tdd-testing.mdc` | `tests/**/*.py` | `40-pytest-aaa` + `41-tdd-dual-track` + `42-integration-tests` |

### 3.1 삭제된 파일 (11개)

`00-project-guardrails.mdc` · `01-io-contract.mdc` · `10-python-style.mdc` · `20-ecb-architecture.mdc` · `30-entity-domain.mdc` · `31-boundary-screen.mdc` · `32-control-usecase.mdc` · `33-data-repository.mdc` · `40-pytest-aaa.mdc` · `41-tdd-dual-track.mdc` · `42-integration-tests.mdc`

---

## STEP 4 — `.cursorrules` 갱신

### 4.1 변경 항목

| 위치 | 변경 내용 |
|------|-----------|
| `project.references` | `*.mdc` → 5개 파일 **개별 경로** |
| `file_structure` | 주석: `레이어별` → `magicsquare-*.mdc` |
| `ai_behavior` | `.cursor/rules/` 해당 레이어 → `magicsquare-*.mdc` 확인 |

### 4.2 유지 항목

- YAML 8섹션 본문 (project, tdd_rules, forbidden 등) — **내용 변경 없음**
- Report/02 단일 진실 원천 · I/O 계약 · ECB 레이어 정의 문구

---

## STEP 5 — 최종 규칙 트리

```
MagicSquare_/
├── .cursorrules
└── .cursor/rules/
    ├── magicsquare-project.mdc          # alwaysApply
    ├── magicsquare-forbidden.mdc        # alwaysApply
    ├── magicsquare-ecb-architecture.mdc # globs: src/**/*.py
    ├── magicsquare-python-code-style.mdc # globs: **/*.py
    └── magicsquare-tdd-testing.mdc      # globs: tests/**/*.py
```

### 5.1 Cursor에서 확인

1. **Settings → Rules** — 5개 규칙 표시
2. `tests/**/*.py` 열고 채팅 → TDD·pytest 규칙 부착
3. `src/**/*.py` 열고 채팅 → ECB 규칙 부착

---

## STEP 6 — 코드·테스트 영향

| 영역 | 변경 |
|------|------|
| `src/magicsquare/` | 없음 |
| `tests/` | 없음 |
| `pyproject.toml` | 없음 |
| `Report/01` · `Report/02` | 없음 |

**회귀 검증:** `python -m pytest tests/ -q` → **9 passed**

---

## 트레이드오프 및 기술 부채

### 채택한 트레이드오프

- **장점:** 규칙 파일 수 감소, 실습 과제 구조와 일치, `.cursorrules`와 1:1 대응이 명확
- **단점:** boundary만 수정할 때 integration 규칙이 같은 파일에 포함 → **globs로는 분리 불가** (파일 단위 통합 때문)

### 문서 부채 (본 Report로 일부 해소)

- [x] `Report/04` — 5파일 구조 기록 (본 문서)
- [x] `Prompting/04` — 직전 세션 Transcript
- [x] `Report/03` · `Prompting/03` — 당시 기록 명시 + Report/04 링크 (갱신 완료)
- [x] `README.md` — 5파일 구조 반영 (갱신 완료)
- [ ] Report/02 ↔ `.cursorrules` ECB harmonization (Report/03부터 미해결)

---

## 미해결 항목 (변경 없음)

- [ ] Mom Test · 1차 사용자 확정
- [ ] DT-01 (`MagicSquareJudge`) Red 테스트부터 마방진 핵심 구현
- [ ] boundary / control / data 레이어 구현
- [ ] `pytest-cov` CI 및 커버리지 gate
- [ ] ECB 레이어 정의 harmonization (Report/02 vs `.cursorrules`)

---

## 다음 단계 (권장 순서)

1. Cursor **Settings → Rules**에서 5파일 인식 확인
2. `tests/control/test_dt01_*.py` Red → `MagicSquareJudge` Green (Report/02 계약 준수)
3. (선택) TDD 본격화 시 레이어별 `.mdc` **재분리** 검토 — 5파일과 **동시 유지 금지**
4. Report/02 ↔ `.cursorrules` ECB 역할 단일화

---

## 부록 A — 생성·삭제·갱신 파일

| 동작 | 경로 |
|------|------|
| 생성 | `.cursor/rules/magicsquare-project.mdc` |
| 생성 | `.cursor/rules/magicsquare-forbidden.mdc` |
| 생성 | `.cursor/rules/magicsquare-ecb-architecture.mdc` |
| 생성 | `.cursor/rules/magicsquare-python-code-style.mdc` |
| 생성 | `.cursor/rules/magicsquare-tdd-testing.mdc` |
| 삭제 | `.cursor/rules/00~42` 번호 규칙 11개 |
| 갱신 | `.cursorrules` (references, file_structure, ai_behavior) |
| 생성 | `Report/04-magicsquare-rules-consolidation-report.md` |
| 생성 | `Prompting/04-magicsquare-rules-consolidation-prompt.md` |
| 갱신 | `Report/03` · `Prompting/03` · `README.md` (현행 5파일·Report/04 링크) |

---

## 부록 B — 관련 프롬프팅

| 문서 | 설명 |
|------|------|
| `Prompting/04-magicsquare-rules-consolidation-prompt.md` | 본 단계 Cursor 대화 Transcript Export |
| `Prompting/03-cursor-rules-implementation-prompt.md` | Rules 최초 구축·User Entity (11파일 시점) |
| `Report/03-cursor-rules-and-implementation-report.md` | Rules 최초 구축 보고서 |

**세션 참조:** [Rules 5파일 통합](83c2a754-c8f5-4b9c-b19f-9a74f6e0711b)
