# RED 단계 TODO — MagicSquare_xx

> SSOT: [PRD.md](PRD.md) · [`.cursorrules`](../.cursorrules) · [reference.md](../.cursor/skills/magic-square-tdd/reference.md)  
> Dual-Track TDD · **RED 1턴마다 테스트 ID 1묶음** · `tests/`만 수정 · `skip`/`xfail` 금지

**권장 진행 순서:** `D-VAL-04` → `D-VAL-05` → `D-VAL-03` → `D-VAL-01` → `D-VAL-02` → `D-LOC-01` → `D-SOL-01` → `U-IN-01`~`05` → `U-OUT-01`~`02`

---

## 공통 Harness

- [ ] `tests/conftest.py` — `grid_g0`, `grid_g1`, `grid_prd`, `grid_bad_slash` 픽스처 (격자 데이터만, 도메인 로직 없음)
- [ ] `src/entity/constants.py` — `MAGIC_CONSTANT`, `BLANK_CELL_VALUE`, `GRID_SIZE` SSOT (스켈레톤·GREEN 시)

### 격자 SSOT

| 이름 | 용도 | 빈칸 (1-index) |
|------|------|----------------|
| G0 | D-VAL 성공 | 없음 (완전 마방진) |
| G1 | D-LOC-01, D-SOL-01, U-OUT-01 | `(2,3)`, `(4,4)` |
| G_prd | D-LOC 확장(선택) | `(2,4)`, `(3,3)` — PRD §5 슬라이드 |
| G_bad_slash | D-VAL-04 Mom Test | `/` 합 ≠ 34 |

**G1 격자:**

```
16   3   2  13
 5  10   0   8
 9   6   7  12
 4  15  14   0
```

### Invariant 약어 (Logic)

| 약어 | 의미 |
|------|------|
| I-R01 | 4×4 |
| I-R02 | 셀 `0` 또는 `1..16` |
| I-R03 | 빈칸 정확히 2 |
| I-R04 | 1~16 중복 없음 |
| I-R05 | 10선 합 = 34 |
| I-1IDX | 좌표·출력 1-index |
| I-RM | row-major 스캔 |
| I-SSOT | 상수는 `constants.py`만 |
| I-NO-E | entity E001~E005 반환·매핑 금지 |
| I-8 | 성공 `int[6]` |

---

## Track B — Domain / Logic (`tests/entity/`)

> Domain Mock **금지** · Expected RED: `ModuleNotFoundError` / `ImportError` / `pytest.fail("RED: D-xxx …")`

### D-VAL-04 — Mom Test RED 우선 (FR-VAL-04)

- [ ] **RED** `tests/entity/test_d_val_04.py` — `validate_anti_diagonal(grid)` · Given G1 또는 `G_bad_slash` · Then `/` 합 = 34 판정
- [ ] **RED FAIL** `python -m pytest tests/entity/test_d_val_04.py -v`
- [ ] **GREEN** `src/entity/validation.py` (또는 동등) 최소 구현
- [ ] Invariant: I-R05, I-SSOT, I-NO-E

### D-VAL-05 (FR-VAL-05)

- [ ] **RED** `tests/entity/test_d_val_05.py` — `validate_all_lines(grid)` · Given G0 · Then 10선 모두 34 → `True`
- [ ] **RED FAIL** pytest 확인
- [ ] **GREEN** 최소 구현
- [ ] Invariant: I-R01~R05, I-NO-E

### D-VAL-03 (FR-VAL-03)

- [ ] **RED** `tests/entity/test_d_val_03.py` — `validate_main_diagonal(grid)` · Given G0 · Then `\` 합 = 34 → `True`
- [ ] **RED FAIL** pytest 확인
- [ ] **GREEN** 최소 구현

### D-VAL-01 (FR-VAL-01)

- [ ] **RED** `tests/entity/test_d_val_01.py` — `validate_rows(grid)` · Given G0 · Then 행 4개 각각 34
- [ ] **RED FAIL** pytest 확인
- [ ] **GREEN** 최소 구현

### D-VAL-02 (FR-VAL-02)

- [ ] **RED** `tests/entity/test_d_val_02.py` — `validate_cols(grid)` · Given G0 · Then 열 4개 각각 34
- [ ] **RED FAIL** pytest 확인
- [ ] **GREEN** 최소 구현

### D-LOC-01 (FR-LOC-01)

- [ ] **RED** `tests/entity/test_d_loc_01.py` — `find_blank_coords(grid)` · Given G1 · Then `[(2, 3), (4, 4)]` (1-index, row-major)
- [ ] **RED FAIL** `python -m pytest tests/entity/test_d_loc_01.py::test_d_loc_01_blank_coords_row_major -v`
- [ ] **GREEN** `src/entity/loc.py` — `find_blank_coords()` 최소 구현
- [ ] Invariant: I-R01~R03, I-1IDX, I-RM

### D-SOL-01 (FR-SOL-01)

- [ ] **RED** `tests/entity/test_d_sol_01.py` — `solve(grid)` · Given G1 · Then `int[6]` `[r1,c1,n1,r2,c2,n2]` (1-index)
- [ ] **RED FAIL** pytest 확인
- [ ] **GREEN** `src/entity/sol.py` 최소 구현
- [ ] Invariant: I-R01~R04, I-1IDX, I-8 · 해 0/다중은 개수만 (E005/E006는 Boundary)

---

## Track A — UI / Boundary (`tests/boundary/`)

> control Mock **허용** (GREEN 시 entity 미호출 검증) · Expected RED: `ModuleNotFoundError` / `pytest.fail("RED: U-xxx …")`

### U-IN-01 (FR-IN-01)

- [ ] **RED** `tests/boundary/test_u_in_01.py` — `validate_input(None)` → `"E003"` · control/entity 미호출
- [ ] **RED FAIL** pytest 확인
- [ ] **GREEN** `src/boundary/input.py` (또는 동등)

### U-IN-02 (FR-IN-02)

- [ ] **RED** `tests/boundary/test_u_in_02.py` — `grid` 3×3 → `"E001"`
- [ ] **RED FAIL** pytest 확인
- [ ] **GREEN** 최소 구현

### U-IN-03 (FR-IN-03)

- [ ] **RED** `tests/boundary/test_u_in_03.py` — 범위 위반(예: `17`) → `"E003"`
- [ ] **RED FAIL** pytest 확인
- [ ] **GREEN** 최소 구현

### U-IN-04 (FR-IN-04)

- [ ] **RED** `tests/boundary/test_u_in_04.py` — 빈칸 `0` 개수 ≠ 2 → `"E002"`
- [ ] **RED FAIL** pytest 확인
- [ ] **GREEN** 최소 구현

### U-IN-05 (FR-IN-05)

- [ ] **RED** `tests/boundary/test_u_in_05.py` — 1~16 중복 → `"E003"`
- [ ] **RED FAIL** pytest 확인
- [ ] **GREEN** 최소 구현

### U-OUT-01 (FR-OUT-01)

- [ ] **RED** `tests/boundary/test_u_out_01.py` — 유효 G1 성공 → `len(result)==6` 또는 OK · `int[6]` 1-index
- [ ] **RED FAIL** pytest 확인
- [ ] **GREEN** `src/boundary/output.py` (또는 동등)

### U-OUT-02 (FR-OUT-02) — Mom Test SC-2

- [ ] **RED** `tests/boundary/test_u_out_02.py` — 10선 중 1줄 ≠ 34 → `"E004"` + 깨진 줄 식별
- [ ] **RED FAIL** pytest 확인
- [ ] **GREEN** 최소 구현

---

## 설계표 요약 (참고)

### Track A — Boundary

| Test ID | Given | Then (기대값) | Expected RED Failure |
|---------|-------|---------------|----------------------|
| U-IN-01 | `grid=None` | `E003` | `ModuleNotFoundError` / `pytest.fail` |
| U-IN-02 | `grid` 3×3 | `E001` | `ModuleNotFoundError` / `pytest.fail` |
| U-IN-03 | 값 1~16 밖 | `E003` | `ModuleNotFoundError` / `AssertionError` |
| U-IN-04 | 빈칸 ≠ 2 | `E002` | `ModuleNotFoundError` / `AssertionError` |
| U-IN-05 | 1~16 중복 | `E003` | `ModuleNotFoundError` / `AssertionError` |
| U-OUT-01 | 유효 G1 | `int[6]` 또는 OK | `pytest.fail` |
| U-OUT-02 | `/` 등 줄 깨짐 | `E004` + 줄 식별 | `pytest.fail` |

### Track B — Logic

| Test ID | 대상 함수 | Given / Then | Invariant |
|---------|-----------|--------------|-----------|
| D-VAL-04 | `validate_anti_diagonal()` | G1 / G_bad → `/` = 34 | I-R05, I-SSOT, I-NO-E |
| D-VAL-05 | `validate_all_lines()` | G0 → 10선 OK | I-R01~R05, I-NO-E |
| D-VAL-03 | `validate_main_diagonal()` | G0 → `\` = 34 | I-R05, I-NO-E |
| D-VAL-01 | `validate_rows()` | G0 → 행 4×34 | I-R05, I-NO-E |
| D-VAL-02 | `validate_cols()` | G0 → 열 4×34 | I-R05, I-NO-E |
| D-LOC-01 | `find_blank_coords()` | G1 → `[(2,3),(4,4)]` | I-R01~R03, I-1IDX, I-RM |
| D-SOL-01 | `solve()` | G1 → `int[6]` | I-R01~R04, I-1IDX, I-8 |

---

## 1004 이미지와의 차이 (본 프로젝트)

| 항목 | 외부 예시 | MagicSquare_xx |
|------|-----------|----------------|
| D-LOC-01 Then | `[(2,2),(3,3)]` | G1 → `[(2,3),(4,4)]` |
| D-MIS-01 | `find_not_exist_nums()` | **미포함** |
| U-FLOW-02 | `execute()` 0회 | **미포함** (control 별도 설계 시) |

---

## 완료 게이트

- [ ] Logic: `python -m pytest tests/entity/ -v` — RED 단계별 FAIL → GREEN PASS
- [ ] UI: `python -m pytest tests/boundary/ -v` — RED 단계별 FAIL → GREEN PASS
- [ ] REFACTOR: Track별 전체 회귀 0 failed
- [ ] README / Report에 진행 상태 반영 (선택)
