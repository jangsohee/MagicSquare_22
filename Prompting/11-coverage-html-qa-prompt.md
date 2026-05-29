# Magic Square — 커버리지 HTML QA (transcript)
_Exported on 2026-05-29 from Cursor — htmlcov 생성 실패 진단 → workaround 검증 → Report/11 Export_  
_선행: `Report/10`, `Report/08`, `defect_list.md`, `README.md`_

---

**User**

커버리지를 html로 확인하려면 어떻게 해야해?

---

**Cursor**

pytest-cov + `--cov-report=html` 사용 안내.

**준비**
```powershell
pip install -e ".[dev]"
```

**HTML 생성 (README 기준)**
```powershell
python -m pytest tests/entity/ --cov=src --cov-report=html
start htmlcov\index.html
```

**주의:** boundary 수집 ERROR 시 전체 pytest는 htmlcov 미생성 가능 (DEF-004).

---

**User**

에러 발생해

---

**Cursor**

터미널 로그 확인.

**증상**
```
ModuleNotFoundError: No module named 'magicsquare.entity.services'
Interrupted: 4 errors during collection
```

**원인:** Report/10 RED Skeleton `test_d_*.py` 4파일이 미구현 모듈을 import.  
Report/08 시점의 `tests/entity/`만 실행 workaround는 Skeleton 추가 후 **무효**.

**검증된 workaround**

1. User 단독 (권장, exit 0):
```powershell
python -m pytest tests/entity/test_user.py --cov=src --cov-report=html
start htmlcov\index.html
```
→ 9 passed, htmlcov 생성 확인

2. entity 전체 + ERROR 무시 (exit 1):
```powershell
python -m pytest tests/entity/ --continue-on-collection-errors --cov=src --cov-report=html
```

| 명령 | 결과 |
|------|------|
| `tests/entity/` | 4 errors → HTML ❌ |
| `test_user.py` | 9 passed → HTML ✅ |
| `--continue-on-collection-errors` | 9 passed + 4 errors → HTML ✅ |

---

**User**

Report 폴더에 보고서 생성하고, Prompting 폴더에 Transcript도 Export 해줘

---

**Cursor**

- `Report/11-coverage-html-qa-report.md` — 원인 분석, 실행 매트릭스, DEF-004 연계
- `Prompting/11-coverage-html-qa-prompt.md` (본 문서)
- `README.md` — 커버리지 HTML 명령 갱신

---

## 재사용 프롬프트 (RED 단계 커버리지 HTML)

```markdown
목표: htmlcov/ 생성 (Green User Entity 기준)

RED 단계 주의:
- test_d_*.py, test_u_*.py, boundary → collection ERROR
- tests/entity/ 전체 실행 시 Skeleton import 실패

권장:
python -m pytest tests/entity/test_user.py --cov=src --cov-report=html
start htmlcov\index.html

대안:
python -m pytest tests/entity/ --continue-on-collection-errors --cov=src --cov-report=html
```

---

## 관련 문서

| 문서 | 경로 |
|------|------|
| 본 단계 보고서 | `Report/11-coverage-html-qa-report.md` |
| RED Skeleton | `Report/10-dual-track-red-skeleton-report.md` |
| 결함 목록 | `defect_list.md` (DEF-004) |
