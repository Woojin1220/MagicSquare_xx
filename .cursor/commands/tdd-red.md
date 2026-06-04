# TDD RED — 실패 테스트 먼저

MagicSquare_xx / **MagicSquare_1004** Dual-Track TDD — **RED 단계만**.  
헌법: [`.cursorrules`](../../.cursorrules) · 절차 상세: [`.cursor/skills/magic-square-tdd/SKILL.md`](../skills/magic-square-tdd/SKILL.md) · ID: [`reference.md`](../skills/magic-square-tdd/reference.md)

---

## 필수 선언

**응답 첫 줄 (고정 형식):**

```
Phase: RED | Layer: <entity|control|boundary> | Track: <Logic|UI> | ID: <D-xxx|U-xxx>
```

예: `Phase: RED | Layer: entity | Track: Logic | ID: D-VAL-04`

---

## 절차

1. **ID 확인** — `reference.md`·`docs/PRD.md` C2C에서 이번 RED **1묶음**만 선택. Mom Test 우선: `D-VAL-04` (`/`) → `D-VAL-05`.
2. **파일** — Logic: `tests/entity/test_d_*.py` 또는 `tests/control/test_d_*.py` · UI: `tests/boundary/test_u_*.py`.
3. **스켈레톤(선택)** — 구현 전 `pytest.fail("RED: <ID> …")`만 두고 FAIL 확인 가능.
4. **AAA 테스트** — **Arrange** 4×4 격자(빈칸 2, 10선 맥락) · **Act** (import 대상은 스텁/미구현 허용) · **Assert** 실패 조건. docstring에 `D-*` / `FR-*` 명시.
5. **pytest FAIL** — 아래 명령 실행 → 터미널 **FAILED** 확인. PASS면 RED 미완( assert·픽스처 조정).
6. **범위** — 이번 턴 변경은 **`tests/`만**. `src/` 수정 없음.

| Track | Layer | 경로 |
|-------|-------|------|
| Logic | entity / control | `tests/entity/`, `tests/control/` |
| UI | boundary | `tests/boundary/` |

---

## pytest 예시 (bash)

```bash
cd MagicSquare_xx
pip install -e ".[dev]"

# Logic — entity (Mom Test: 반대 대각선)
python -m pytest tests/entity/test_d_val_04.py::test_d_val_04_anti_diagonal_sum_34 -v

# Logic — control
python -m pytest tests/control/test_d_*.py::<test_name> -v

# UI — boundary
python -m pytest tests/boundary/test_u_in_01.py::<test_name> -v

# 수집 확인
python -m pytest --collect-only tests/entity/test_d_val_04.py
```

**기대:** `FAILED` + `AssertionError` / `ModuleNotFoundError` / `pytest.fail("RED: …")` 등 — **통과(PASSED)는 RED 실패**.

---

## 보고

| 항목 | 내용 |
|------|------|
| **테스트 ID** | 예: `D-VAL-04` |
| **FAIL 요약** | pytest 출력 1~3줄 인용 (FAILED 이유) |
| **변경 파일** | `tests/` 아래 경로만 나열 |
| **Track / Layer** | Logic·entity 등 |
| **다음** | GREEN 대기 — `src/` 구현은 별도 Command·요청 |

**commit / push 하지 않음** (사용자 요청 시만).

---

## 금지

| 금지 | 이유 |
|------|------|
| **`src/` 수정** (import·스텁 파일 추가 포함) | RED = 테스트만 |
| **Logic Track Domain Mock** | `unittest.mock`으로 entity/핵심 도메인 대체 금지 |
| **assert 완화·삭제** | 통과로 우회 |
| **`skip` / `xfail`** | Mom Test·Loop 무력화 |
| **다음 ID 선행 RED/GREEN** | 1묶음씩 |
| **GREEN·REFACTOR 혼합** | Phase RED만 |

**허용:** UI Track에서 entity/control **Mock** · `tests/conftest.py` 픽스처 · `pytest.fail("RED: …")` 스켈레톤.
