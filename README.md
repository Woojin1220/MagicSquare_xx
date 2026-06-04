# MagicSquare_xx

4×4 **부분 마방진**(빈칸 2개)에서 **10선 합=34** 판정을 빠짐없이·기계적으로 수행하고, 깨진 줄(특히 **`/`**)을 즉시 식별하는 TDD · ECB 프로젝트입니다.

**상세 스펙:** [docs/PRD.md](docs/PRD.md)

---

## 배경 (Mom Test)

학습자가 **특정 행·열부터** 합을 맞추고 `\`·`/`까지 본 뒤 **맞다고 제출**했으나 **채점**에서 오답. 재풀이 중 **반대 대각선 `/` 합** 오류를 발견했고 **약 10분** 추가 소요 ([PRD §1](docs/PRD.md#1-배경-mom-test)).

| 항목 | 내용 |
|------|------|
| **페르소나** | 4×4 부분 마방진을 손으로/코드로 다루는 학습자 |
| **진짜 문제** | 손 검증·`/`` 34 비교 후에도 채점 오답 → `/` 합 오류 · **10분** |
| **증거** | 「행·열부터 맞춤」 / 「맞다고 넘어감」 / 「채점→10분→반대 대각선」 |
| **표면 문제 (비목표)** | 검증/풀이 프로그램·PyQt 완성 앱·ECB 설계 완성만 목표로 삼기 |

## 핵심 질문 ([PRD §12](docs/PRD.md#12-핵심-질문))

> **4×4 격자에서 빈칸 2개를 채운 결과가 부분 마방진 조건(10선=34)을 만족하는가?**

## 목표 · 비목표

**목표** ([PRD §2](docs/PRD.md#2-목표))

- 10선 합 **34** 검증 · 실패 시 **줄 식별**(행/열/`\`/`/`)
- 빈칸 좌표·후보 판정 (Logic Track)
- **채점 전** SC-1~3 충족 (채점 후 10분 재작업 방지)

**비목표** ([PRD §3](docs/PRD.md#3-비목표))

- PyQt 상용 앱 · 배포
- 3×3 / 5×5 / 자동 생성
- 세션 3 Domain GREEN · UI **완료**
- 수동 “대충 맞음” 확인만으로 완료

## 도메인 규칙 ([PRD §5](docs/PRD.md#5-도메인-규칙))

| 규칙 | 설명 |
|------|------|
| R-01 | 격자 **4×4** |
| R-02 | 셀: `0`(빈칸) 또는 `1..16` |
| R-03 | 빈칸 **정확히 2개** |
| R-04 | 1~16 **중복 없음** |
| R-05 | **10선** 각각 합 = **34** |
| R-06 | 10선 = 행4 + 열4 + `\` + `/` |

### 예시 격자 (슬라이드 4.1)

| | c1 | c2 | c3 | c4 |
|---|----|----|----|-----|
| r1 | 16 | 3 | 2 | 13 |
| r2 | 5 | 10 | 11 | **0** |
| r3 | 9 | 6 | **0** | 12 |
| r4 | 4 | 15 | 14 | 1 |

빈칸: (r2,c4), (r3,c3).

## 성공 기준 ([PRD §7](docs/PRD.md#7-성공-기준-mom-test))

| ID | 기준 | Mom Test |
|----|------|----------|
| SC-1 | 10선 합 **전부** 검증 (`\`·`/` 포함) | 「행·열부터 맞춤」 |
| SC-2 | ≠34 → 실패 + **줄 식별** | 「맞다고 넘어감」+ 「반대 대각선」 |
| SC-3 | 원인 줄 특정 **1분 이내** | 「10분」+ 「처음부터 다시」 |

## 문제 인식 조건 ([PRD §6.5](docs/PRD.md#65-문제-인식-조건-슬라이드--3개-이상))

| # | 조건 |
|---|------|
| P-01 | 10선 중 한 줄 합 ≠ 34 (예: `/`) |
| P-02 | 빈칸 개수 ≠ 2 |
| P-03 | 1~16 중복 또는 범위 위반 |
| P-04 | (선택) 빈칸 미채움 상태에서 완료 |

## 에러 코드 ([PRD §10](docs/PRD.md#10-에러-코드))

| 코드 | 의미 |
|------|------|
| E001 | 크기 ≠ 4×4 |
| E002 | 빈칸 ≠ 2 |
| E003 | 범위·중복·null |
| E004 | 특정 줄 합 ≠ 34 |

## 아키텍처 ([PRD §9](docs/PRD.md#9-아키텍처-ecb--슬라이드))

| 계층 | 책임 | 후보 |
|------|------|------|
| **Entity** | 격자·셀·판정 | `MagicSquare`, `Cell`, `SolveResult` |
| **Control** | 검증·탐색·풀이 | `SquareValidator`, `MissingFinder`, `Solver` |
| **Boundary** | I/O·표시 | `GridUI`, `InputHandler`, `ResultDisplay` |

- **Dual-Track TDD:** Logic `D-*` + UI `U-*`
- **RED 우선:** pytest FAIL → GREEN → REFACTOR

### 세션 3 산출

| 계층 | 산출 |
|------|------|
| Rule | `.cursorrules` |
| Command | `/tdd-red`, `/pytest-logic` |
| Skill | `magic-square-tdd` |
| Test Loop | pytest RED → FAIL |

## RED 단계 진행 목록

> 상세 체크리스트·설계표: **[docs/RED-TODO.md](docs/RED-TODO.md)**  
> 규칙: **RED 1턴 = 테스트 ID 1묶음** · 변경은 `tests/`만 · `skip`/`xfail` 금지 · Logic Track Domain Mock 금지

**권장 순서:** `D-VAL-04` → `D-VAL-05` → `D-VAL-03` → `D-VAL-01` → `D-VAL-02` → `D-LOC-01` → `D-SOL-01` → `U-IN-01`~`05` → `U-OUT-01`~`02`

### 공통 Harness (RED 선행)

- [ ] `tests/conftest.py` — `grid_g0`, `grid_g1`, `grid_prd`, `grid_bad_slash` (격자만, 로직 없음)
- [ ] `src/entity/constants.py` — `MAGIC_CONSTANT`, `BLANK_CELL_VALUE`, `GRID_SIZE` (스켈레톤·GREEN 시)

**G1 격자 (RED SSOT)** — 빈칸 1-index `(2,3)`, `(4,4)`:

```
16   3   2  13
 5  10   0   8
 9   6   7  12
 4  15  14   0
```

### Track B — Logic (`tests/entity/`)

| Test ID | RED 작업 | pytest (예시) | 상태 |
|---------|----------|---------------|------|
| D-VAL-04 | `test_d_val_04.py` — `validate_anti_diagonal()` · `/` 합 34 (Mom Test **우선**) | `pytest tests/entity/test_d_val_04.py -v` | ⏳ |
| D-VAL-05 | `test_d_val_05.py` — `validate_all_lines()` · G0 · 10선 OK | `pytest tests/entity/test_d_val_05.py -v` | ⏳ |
| D-VAL-03 | `test_d_val_03.py` — `validate_main_diagonal()` · G0 · `\` = 34 | `pytest tests/entity/test_d_val_03.py -v` | ⏳ |
| D-VAL-01 | `test_d_val_01.py` — `validate_rows()` · G0 · 행 4×34 | `pytest tests/entity/test_d_val_01.py -v` | ⏳ |
| D-VAL-02 | `test_d_val_02.py` — `validate_cols()` · G0 · 열 4×34 | `pytest tests/entity/test_d_val_02.py -v` | ⏳ |
| D-LOC-01 | `test_d_loc_01.py` — `find_blank_coords()` · G1 → `[(2,3),(4,4)]` | `pytest tests/entity/test_d_loc_01.py::test_d_loc_01_blank_coords_row_major -v` | ⏳ |
| D-SOL-01 | `test_d_sol_01.py` — `solve()` · G1 → `int[6]` 1-index | `pytest tests/entity/test_d_sol_01.py -v` | ⏳ |

**Logic RED 게이트:** 각 ID마다 터미널 **FAILED** (`ModuleNotFoundError` / `pytest.fail("RED: D-xxx …")`) 확인 후 GREEN.

### Track A — UI (`tests/boundary/`)

| Test ID | RED 작업 | Then (기대) | 상태 |
|---------|----------|-------------|------|
| U-IN-01 | `test_u_in_01.py` — `grid=None` | `E003` | ⏳ |
| U-IN-02 | `test_u_in_02.py` — `grid` 3×3 | `E001` | ⏳ |
| U-IN-03 | `test_u_in_03.py` — 값 1~16 밖 | `E003` | ⏳ |
| U-IN-04 | `test_u_in_04.py` — 빈칸 ≠ 2 | `E002` | ⏳ |
| U-IN-05 | `test_u_in_05.py` — 1~16 중복 | `E003` | ⏳ |
| U-OUT-01 | `test_u_out_01.py` — 유효 G1 | `int[6]` 또는 OK | ⏳ |
| U-OUT-02 | `test_u_out_02.py` — 줄 깨짐 (Mom Test SC-2) | `E004` + 줄 식별 | ⏳ |

**UI RED 게이트:** control Mock 허용 · `pytest tests/boundary/test_u_*.py -v` → **FAILED** 확인.

### RED 완료 게이트

- [ ] Logic: `pytest tests/entity/ -v` — ID별 RED FAIL 확보
- [ ] UI: `pytest tests/boundary/ -v` — ID별 RED FAIL 확보
- [ ] 이후 GREEN → REFACTOR ([docs/RED-TODO.md](docs/RED-TODO.md) GREEN 항목 참고)

## C2C 요약 ([PRD §8](docs/PRD.md#8-c2c-추적-예시))

| Test ID | PRD | Layer | 요약 |
|---------|-----|-------|------|
| D-VAL-04 | FR-VAL-04 | entity | `/` 합 = 34 (**RED 우선**) |
| D-VAL-05 | FR-VAL-05 | entity | 10선 전체 |
| D-VAL-03 | FR-VAL-03 | entity | `\` 합 = 34 |
| D-VAL-01 | FR-VAL-01 | entity | 행 4 — 합 34 |
| D-VAL-02 | FR-VAL-02 | entity | 열 4 — 합 34 |
| D-LOC-01 | FR-LOC-01 | entity | 빈칸 2좌표 (1-index) |
| D-SOL-01 | FR-SOL-01 | entity | 빈칸 대입 · `int[6]` |
| U-IN-01~05 | FR-IN-01~05 | boundary | 입력 검증 |
| U-OUT-01~02 | FR-OUT-01~02 | boundary | 성공/실패 출력 |

## 사용자 ([PRD §4](docs/PRD.md#4-사용자))

- **Primary:** 4×4 부분 마방진 과제 학습자
- **Secondary:** TDD / ECB / Cursor 워크플로 실습자

## 문서

| 문서 | 설명 |
|------|------|
| [docs/PRD.md](docs/PRD.md) | **SSOT** — FR/SC/C2C/ECB/에러 코드 |
| [docs/RED-TODO.md](docs/RED-TODO.md) | **RED/GREEN 체크리스트** — Dual-Track 설계표·픽스처·Invariant |
| [Report/01.MagicSquare_ProblemDefinition_Report.md](Report/01.MagicSquare_ProblemDefinition_Report.md) | Mom Test · 세션 3 워크북 |
| [Prompt/01.MagicSquare_Session1_MomTest_ProblemDefinition-Transcript.md](Prompt/01.MagicSquare_Session1_MomTest_ProblemDefinition-Transcript.md) | 세션 1 Transcript |

## 프로젝트 구조

```
MagicSquare_xx/
├── README.md
├── .cursorrules
├── docs/
│   ├── PRD.md
│   └── RED-TODO.md          # RED/GREEN 체크리스트
├── Report/01.*.md
├── Prompt/01.*-Transcript.md
├── src/{entity,control,boundary}/
└── tests/
    ├── conftest.py          # grid_g0, grid_g1, … (RED 예정)
    ├── entity/              # test_d_*.py
    ├── control/
    └── boundary/            # test_u_*.py
```

## 개발 환경

```bash
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install -e ".[dev]"

# RED — 단일 ID (Mom Test 우선)
python -m pytest tests/entity/test_d_val_04.py -v

# RED — Logic / UI 전체 (진행 후)
python -m pytest tests/entity/ -v
python -m pytest tests/boundary/ -v
```

## 다음 단계 ([PRD §13](docs/PRD.md#13-다음-단계))

1. [docs/RED-TODO.md](docs/RED-TODO.md) — Harness `conftest` + **D-VAL-04** RED 스켈레톤
2. `pytest` **FAILED** 로그 확보 → GREEN은 ID 1묶음씩
3. Logic Track 완료 후 Boundary `U-IN-*` → `U-OUT-*` RED
4. Mom Test Q11 보완(선택)

## 용어 ([PRD §11](docs/PRD.md#11-용어))

| 용어 | 정의 |
|------|------|
| 마법 상수 | **34** |
| 10선 | 행4 + 열4 + `\` + `/` |
| 빈칸 | `0`인 셀 (**2개**) |
| 부분 마방진 | 빈칸 2개를 채우면 완전 마방진이 되는 4×4 격자 |
