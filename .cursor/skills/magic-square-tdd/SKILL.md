---
name: magic-square-tdd
description: MagicSquare_1004 Dual-Track TDD·ECB 개발 시 Agent가 따를 절차. RED/GREEN/REFACTOR, pytest Loop, Logic/UI Track, E001~E007·Mock 규칙. Use for MagicSquare_xx/1004, D-VAL·U-IN, entity/control/boundary, pytest, TDD, ECB, 10선, 마방진.
---

# magic-square-tdd

헌법: [`.cursorrules`](../../../.cursorrules) · 요구: [`docs/PRD.md`](../../../docs/PRD.md) · 테스트 ID: [`reference.md`](reference.md)

## 언제 이 Skill을 켜는지

다음 **하나라도** 해당하면 본 Skill을 적용한다.

- `MagicSquare_xx` / 부분 마방진 / **10선=34** / 빈칸 2개 도메인 코드·테스트 작업
- **RED · GREEN · REFACTOR** 단계 진행, `test_d_*` / `test_u_*` 작성
- **Logic Track**(`tests/entity`, `tests/control`) 또는 **UI Track**(`tests/boundary`)
- ECB 위반·Mock·E001~E007·`constants.py` SSOT 검토
- Mom Test 재현: **D-VAL-04** (`/`) → **D-VAL-05** (10선)

**끄거나 축소:** 문서만 편집(Report/Prompt), git만, PyQt 완성 앱·3×3/5×5 확장.

---

## 응답 형식 (매 턴)

맨 앞 한 줄:

`Phase(RED|GREEN|REFACTOR) · Layer(entity|control|boundary) · Track(Logic|UI) · ID(D-xxx|U-xxx)`

이후 한국어로 진행. **commit/push는 사용자 요청 시만.**

---

## Logic Track vs UI Track

| | Logic Track | UI Track |
|---|-------------|----------|
| **Layer** | entity, control | boundary |
| **테스트 ID** | `D-*` | `U-*` |
| **경로** | `tests/entity/`, `tests/control/` | `tests/boundary/` |
| **파일명** | `test_d_*.py` | `test_u_*.py` |
| **Mock** | Domain Mock **금지** (실제 entity/control) | entity·control Mock **허용** |
| **import** | `boundary` 테스트에서 실 entity 금지 (UI는 Mock) | — |

**ECB:** `boundary → control → entity` · `control → entity`만 허용 · `entity → control/boundary` **금지** · `control → boundary` **금지**

---

## ECB · Mock · E001~E007

| 구분 | 허용 | 금지 |
|------|------|------|
| **Entity** | 줄 합 판정, 빈칸 좌표, 후보·해 개수 등 **도메인 값** | `E001`~`E005` 문자열·코드 반환·사용자 메시지 매핑 |
| **Control** | entity 호출·흐름 조합 | boundary import, E00x 직접 노출 |
| **Boundary** | 입력 검증 → **E001~E007**, `int[6]` 1-index 출력 | 도메인 알고리즘 구현 |
| **Logic 테스트** | 실제 `src/entity` (및 control) | `unittest.mock`으로 entity/핵심 도메인 대체 |
| **UI 테스트** | boundary + Mock entity/control | — |

| 코드 | Boundary | Entity |
|------|----------|--------|
| E001 | 크기 ≠ 4×4 | 처리 금지 |
| E002 | 빈칸 ≠ 2 | 처리 금지 |
| E003 | 범위·중복·null | 처리 금지 |
| E004 | 줄 합 ≠ 34 | 처리 금지 (판정만) |
| E005 | 풀이 없음 | 처리 금지 |
| E006 | 풀이 다중 | entity는 개수·후보만, 코드 부여는 Boundary |
| E007 | I/O·표현 오류 | — |

**MagicConstant:** `34`/`16`/`4`/`0` → `src/entity/constants.py`만. 리터럴 산재 금지.

---

## RED (5~7단계)

1. **선언:** Phase·Layer·Track·대상 ID (`reference.md`·PRD C2C 확인).
2. **범위:** 이번 RED는 **테스트 1 ID(1묶음)** 만. `tests/`만 수정.
3. **스켈레톤(선택):** `test_d_*.py` + `pytest.fail("RED: D-VAL-04 …")` — 아직 `src/` 로직 없음.
4. **RED 본문:** Arrange(4×4 격자·Mom Test `/` 깨짐 케이스) · Act · Assert — docstring에 `D-*`·`FR-*` 명시.
5. **실행:** Logic → `python -m pytest tests/entity/<file>::<test> -v` (또는 `tests/control/`).
6. **게이트:** 터미널에 **FAILED** + 기대 메시지 확인. 통과하면 RED 아님 → assert/픽스처 수정.
7. **금지 확인:** `src/` 구현 추가 없음, skip/xfail 없음.

**Mom Test 우선 순서:** `D-VAL-04` → `D-VAL-05` → `D-LOC-01` → …

---

## GREEN (5~7단계)

1. **선언:** 동일 ID·Track. RED FAIL 로그가 있는 상태에서만 시작.
2. **범위:** 이번 GREEN은 **RED 1묶음을 통과시키는 최소** `src/`만 수정.
3. **구현:** Layer 준수 — entity 판정, control 조합, boundary는 U-* 시만.
4. **SSOT:** 상수는 `constants.py`에서 import.
5. **실행:** 해당 테스트 파일 → 통과 확인.
6. **확장(선택):** 같은 Track `pytest tests/entity/ -v` 회귀 — **0 failed**.
7. **금지:** assert 완화·테스트 삭제·다음 ID 선행 구현.

---

## REFACTOR (5~7단계)

1. **선언:** Phase REFACTOR · GREEN 통과 직후만.
2. **범위:** 동작 동일·공개 API·테스트 ID 계약 유지.
3. **대상:** 중복 합 계산, 명명, control/entity 책임 분리 등.
4. **실행:** Logic 전체 `pytest tests/entity/ tests/control/ -v` · UI `pytest tests/boundary/ -v`.
5. **Golden Master(해당 시):** `tests/golden/*.approved.txt` — **`UPDATE_GOLDEN=1`은 사용자 명시 승인 후만**. 임의 스냅샷 갱신 금지.
6. **ECB 재검:** import 방향·Mock 규칙 위반 없음.
7. **완료:** 리팩터 전후 동일 pytest green.

---

## Test / Review Loop — pytest 언제 돌리는지

| 시점 | 명령 | 기대 |
|------|------|------|
| RED 직후 | `pytest <단일 테스트> -v` | **FAIL** (증거 로그 보관) |
| GREEN 직후 | 동일 단일 테스트 | **PASS** |
| GREEN 회귀 | `pytest tests/entity/ -v` (+ control) | PASS |
| UI RED/GREEN | `pytest tests/boundary/<file> -v` | FAIL → PASS |
| REFACTOR | Track별 디렉터리 전체 | 전부 PASS |
| 수집만 | `pytest --collect-only tests/` | ID·경로 확인 (0 collected는 테스트 없을 때만 정상) |
| Harness 점검 | `pip install -e ".[dev]"` 후 상기 | `pyproject.toml` `pythonpath=["src"]` |

**Loop 증거:** “통과했다”는 **터미널 출력 인용**이 없으면 완료로 보고하지 않는다.

**Hook과의 관계:** Hook이 pytest 힌트를 줄 수 있으나 **판정·Phase 전환은 본 Skill + `.cursorrules`가 우선**.

---

## 10선 체크리스트 (수동·설계용)

손 검증·테스트 Arrange 시 **10개 모두** 명시:

`R1 R2 R3 R4 · C1 C2 C3 C4 · \ · /` — 각 합 **34**.

---

## 완료 보고 항목

작업 마칠 때 아래를 **짧게** 채운다.

| 항목 | 내용 |
|------|------|
| Phase / Track / ID | 예: RED · Logic · D-VAL-04 |
| 변경 파일 | `tests/...`, `src/...` |
| pytest 결과 | 명령 + FAILED/PASSED 한 줄 인용 |
| ECB | import·Mock 위반 여부 (없음/수정함) |
| E00x | Boundary만 사용 여부 |
| Mom Test | `/`·10선·SC-1~2 연결 여부 |
| 미완 | 다음 RED ID, Blocker |
| commit | **하지 않음** (요청 시만) |

---

## 참고

- 상세 테스트 ID: [`reference.md`](reference.md)
- Command(`/tdd-red` 등)는 별도 파일 — 없으면 본 Skill 절차를 직접 따른다.
