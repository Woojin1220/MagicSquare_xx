"""D-SOL-01 — FR-SOL-01: solve (G1 Step A, int[6] 1-index)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from _approval import assert_matches_golden
from entity.sol import solve

GOLDEN_D_SOL_01_G1_STEP_A = "d_sol_01_g1_step_a.approved.txt"


def _format_solution_golden(result: list[int]) -> str:
    return f"# Test ID: D-SOL-01\n{result!r}"


def test_d_sol_01_step_a_success(grid_g1):
    # Given: G1 격자 (빈칸 2개, 10선=34 성립)
    # When: solve(grid_g1) 호출
    # Then: int[6] [r1,c1,n1,r2,c2,n2] — 1-index, row-major
    result = solve(grid_g1)
    assert result == [2, 3, 11, 4, 4, 1]
    assert_matches_golden(_format_solution_golden(result), GOLDEN_D_SOL_01_G1_STEP_A)
