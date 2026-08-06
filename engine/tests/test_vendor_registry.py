"""EVAL-004 — Vendor registry must validate and must not invent scores."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

jsonschema = pytest.importorskip("jsonschema")

_ROOT = Path(__file__).resolve().parents[2]
_REG_DIR = _ROOT / "evaluation" / "vendor_registry"


def test_registry_validates_against_schema() -> None:
    schema = json.loads((_REG_DIR / "schema.json").read_text(encoding="utf-8"))
    instance = json.loads((_REG_DIR / "registry.json").read_text(encoding="utf-8"))
    jsonschema.validate(instance=instance, schema=schema)
    assert instance["contains_personal_data"] is False
    assert instance["entries"] == []


def test_schema_rejects_floating_latest_as_required_field_presence() -> None:
    """Document policy: source_version is required on entries; empty registry OK."""
    schema = json.loads((_REG_DIR / "schema.json").read_text(encoding="utf-8"))
    bad = {
        "schema_version": "0.1.0",
        "registry_id": "x",
        "contains_personal_data": False,
        "entries": [
            {
                "vendor_id": "example",
                "display_name": "Example",
                "source": "https://example.invalid",
                # missing source_version
                "capabilities": [],
                "measurement_status": "NOT_MEASURED",
            }
        ],
    }
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=bad, schema=schema)
