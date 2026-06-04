"""Blank cell location (FR-LOC-01)."""

from entity.constants import BLANK_CELL_VALUE


def find_blank_coords(grid: list[list[int]]) -> list[tuple[int, int]]:
    """Return 1-indexed (row, col) of blank cells in row-major order."""
    coords: list[tuple[int, int]] = []
    for row_idx, row in enumerate(grid):
        for col_idx, value in enumerate(row):
            if value == BLANK_CELL_VALUE:
                coords.append((row_idx + 1, col_idx + 1))
    return coords
