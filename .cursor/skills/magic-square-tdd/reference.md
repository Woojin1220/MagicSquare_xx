# D-* · U-* 테스트 ID (MagicSquare_xx)

> PRD C2C: [`docs/PRD.md`](../../../docs/PRD.md) §6·§8

## Logic Track (`D-*`)

| ID | PRD | Layer | 요약 |
|----|-----|-------|------|
| D-VAL-01 | FR-VAL-01 | entity | 행 4 — 합 34 |
| D-VAL-02 | FR-VAL-02 | entity | 열 4 — 합 34 |
| D-VAL-03 | FR-VAL-03 | entity | 주대각선 `\` — 합 34 |
| D-VAL-04 | FR-VAL-04 | entity | 반대 대각선 `/` — 합 34 (**RED 우선**) |
| D-VAL-05 | FR-VAL-05 | entity | 10선 전체 — 합 34 |
| D-LOC-01 | FR-LOC-01 | entity | 빈칸 2곳 좌표 |
| D-SOL-01 | FR-SOL-01 | entity | 빈칸 대입 풀이 · `int[6]` 1-index |

## UI Track (`U-*`)

| ID | PRD | Layer | 요약 |
|----|-----|-------|------|
| U-IN-01 | FR-IN-01 | boundary | `grid is None` → E003 |
| U-IN-02 | FR-IN-02 | boundary | 크기 ≠ 4×4 → E001 |
| U-IN-03 | FR-IN-03 | boundary | 범위 위반 → E003 |
| U-IN-04 | FR-IN-04 | boundary | 빈칸 ≠ 2 → E002 |
| U-IN-05 | FR-IN-05 | boundary | 중복 → E003 |
| U-OUT-01 | FR-OUT-01 | boundary | 성공 출력 |
| U-OUT-02 | FR-OUT-02 | boundary | 실패 + 줄 식별 (E004 등) |

**RED 권장 순서:** `D-VAL-04` → `D-VAL-05` → `D-LOC-01` → `D-SOL-01` → `U-IN-*`
