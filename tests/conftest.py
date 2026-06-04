"""Shared pytest fixtures — grid data only (no domain logic)."""

import pytest

__all__ = ["grid_g1"]


@pytest.fixture
def grid_g1():
    """G1 — 4×4, 빈칸(0) 2개; row-major 1-index blanks (2,3), (4,4)."""
    return [
        [16, 3, 2, 13],
        [5, 10, 0, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 0],
    ]
