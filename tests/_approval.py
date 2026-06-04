"""Approval test helpers — Golden Master (tests/golden/*.approved.txt)."""

import os
from pathlib import Path

GOLDEN_DIR = Path(__file__).resolve().parent / "golden"


def assert_matches_golden(actual: str, relative: str) -> None:
    path = GOLDEN_DIR / relative
    if os.environ.get("UPDATE_GOLDEN") == "1":
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(actual, encoding="utf-8")
        return
    expected = path.read_text(encoding="utf-8")
    assert actual == expected, (
        f"Golden mismatch:\n{path}\n--- expected ---\n{expected}\n--- actual ---\n{actual}"
    )
