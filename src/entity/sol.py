"""FR-SOL-01 — blank cell solver (entity)."""

from entity.constants import (
    BLANK_CELL_VALUE,
    GRID_SIZE,
    MAGIC_CONSTANT,
    MAX_CELL_VALUE,
)
from entity.loc import find_blank_coords


def _all_lines_sum_to_magic(grid: list[list[int]]) -> bool:
    for row in range(GRID_SIZE):
        if sum(grid[row][col] for col in range(GRID_SIZE)) != MAGIC_CONSTANT:
            return False
    for col in range(GRID_SIZE):
        if sum(grid[row][col] for row in range(GRID_SIZE)) != MAGIC_CONSTANT:
            return False
    if sum(grid[i][i] for i in range(GRID_SIZE)) != MAGIC_CONSTANT:
        return False
    if sum(grid[i][GRID_SIZE - 1 - i] for i in range(GRID_SIZE)) != MAGIC_CONSTANT:
        return False
    return True


def _missing_values(grid: list[list[int]]) -> list[int]:
    used = {
        grid[row][col]
        for row in range(GRID_SIZE)
        for col in range(GRID_SIZE)
        if grid[row][col] != BLANK_CELL_VALUE
    }
    return [value for value in range(1, MAX_CELL_VALUE + 1) if value not in used]


def solve(grid: list[list[int]]) -> list[int] | None:
    """Return int[6] [r1, c1, n1, r2, c2, n2] (1-index) or None if no solution."""
    (r1, c1), (r2, c2) = find_blank_coords(grid)
    missing = _missing_values(grid)
    for i, n1 in enumerate(missing):
        for n2 in missing[i + 1 :]:
            for v1, v2 in ((n1, n2), (n2, n1)):
                trial = [row[:] for row in grid]
                trial[r1 - 1][c1 - 1] = v1
                trial[r2 - 1][c2 - 1] = v2
                if _all_lines_sum_to_magic(trial):
                    return [r1, c1, v1, r2, c2, v2]
    return None
