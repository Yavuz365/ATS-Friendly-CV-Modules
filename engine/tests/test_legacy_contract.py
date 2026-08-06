from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator, validate


def test_v151_schema_and_golden_payloads_are_frozen_and_valid():
    root = Path(__file__).parents[2]
    schema_path = root / "schemas" / "v1.5.1" / "report.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)

    examples = sorted((schema_path.parent / "examples").glob("*.json"))
    assert [path.name for path in examples] == ["diagnostic.json", "framework-baseline.json"]
    for path in examples:
        validate(json.loads(path.read_text(encoding="utf-8")), schema)
