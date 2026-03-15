#!/usr/bin/env python3
"""Validate Scoop bucket metadata used by GitHub CI."""

from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
BUCKET_DIR = REPO_ROOT / "bucket"
README_PATH = REPO_ROOT / "README.md"

EXPECTED_README_SNIPPETS = [
    "scoop bucket add cnb-rs https://cnb.cool/wwvo/cnb-rs/scoop-cnb-rs.git",
    "scoop install cnb-rs/cnb-rs",
    "Set-Alias cnb cnb-rs",
]


def validate_manifest(path: Path) -> list[str]:
    errors: list[str] = []
    data = json.loads(path.read_text(encoding="utf-8"))

    bins = data.get("bin", [])
    if "cnb-rs.exe" not in bins:
        errors.append(f"{path.name}: missing cnb-rs.exe in bin")
    if "git-cnb-rs.exe" in bins:
        errors.append(f"{path.name}: git-cnb-rs.exe must not appear in bin")

    notes = data.get("notes", "")
    if "hook" in notes.lower():
        errors.append(f"{path.name}: notes must not mention hook")

    return errors


def validate_readme(path: Path) -> list[str]:
    errors: list[str] = []
    content = path.read_text(encoding="utf-8")

    for snippet in EXPECTED_README_SNIPPETS:
        if snippet not in content:
            errors.append(f"README.md: missing expected snippet: {snippet}")

    return errors


def main() -> int:
    errors: list[str] = []

    for manifest_path in sorted(BUCKET_DIR.glob("*.json")):
        errors.extend(validate_manifest(manifest_path))

    errors.extend(validate_readme(README_PATH))

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("CI metadata validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
