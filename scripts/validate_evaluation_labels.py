#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ALLOWED = {"PASS", "FAIL", "REVIEW", "WARN", "ERROR", "NOT_RUN"}


def validate_labels(path: Path) -> list[str]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    seen: set[tuple[str, str]] = set()
    for index, item in enumerate(payload.get("labels", []), start=1):
        fixture_id = str(item.get("fixture_id", ""))
        task = str(item.get("task", ""))
        label = str(item.get("label", ""))
        key = (fixture_id, task)
        if not fixture_id or not task:
            errors.append(f"label[{index}] fixture_id/task zorunlu")
        if key in seen:
            errors.append(f"duplicate label: {fixture_id}/{task}")
        seen.add(key)
        if label not in ALLOWED:
            errors.append(f"invalid label: {fixture_id}={label}")
        if item.get("reviewed") is not True:
            errors.append(f"unreviewed label: {fixture_id}")
        if not item.get("label_source") or not item.get("reason"):
            errors.append(f"provenance eksik: {fixture_id}")
        if fixture_id == "PDF-SCAN-001" and label == "PASS":
            errors.append("scan fixture OCR olmadan PASS olamaz")
        if fixture_id == "EMPTY-REQUIREMENTS-001" and label == "PASS":
            errors.append("empty requirements PASS olamaz")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    errors = validate_labels(args.path)
    if errors:
        print("\n".join(errors))
        return 1
    print(f"OK: {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
