from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

from ats_engine import parse_document
from ats_engine.errors import DocumentParseError
from ats_engine.field_evaluation import evaluate_fields


def _load_generator(root: Path):
    path = root / "evaluation" / "gold" / "generate_corpus.py"
    spec = importlib.util.spec_from_file_location("ats_gold_generator", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_binary_gold_corpus_matches_manifest(tmp_path):
    root = Path(__file__).parents[2]
    manifest = json.loads((root / "evaluation" / "gold" / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["version"] == "1.0.0"
    assert manifest["contains_personal_data"] is False

    generated = _load_generator(root).generate(tmp_path)
    assert set(generated) == {item["id"] for item in manifest["fixtures"]}

    for fixture in manifest["fixtures"]:
        path = generated[fixture["id"]]
        assert path.is_file() and path.stat().st_size > 0
        if fixture["expected_status"] == "ERROR":
            with pytest.raises(DocumentParseError) as caught:
                parse_document(path)
            assert caught.value.code.value == fixture["expected_error_code"]

            # ING-005: field-level evaluation on the ERROR path
            report = evaluate_fields(
                fixture["id"],
                None,
                expected_status="ERROR",
                expected_error_code=fixture.get("expected_error_code"),
                parse_error_code=caught.value.code.value,
                required_text=fixture.get("required_text", []),
                structural_features=fixture.get("structural_features", {}),
            )
            assert report.all_required_passed is True, fixture["id"]
            continue

        result = parse_document(path)
        assert result.status.value == fixture["expected_status"]
        assert result.extraction_method in fixture["expected_extraction_methods"]
        for expected_text in fixture["required_text"]:
            assert expected_text in result.text
        for key, expected in fixture.get("structural_features", {}).items():
            assert result.structural_features[key] == expected

        # ING-005: field-level evaluation must also pass
        report = evaluate_fields(
            fixture["id"],
            result,
            expected_status=fixture["expected_status"],
            required_text=fixture.get("required_text", []),
            structural_features=fixture.get("structural_features", {}),
        )
        assert report.all_required_passed is True, (
            fixture["id"],
            [(v.field_name, v.passed, v.detail) for v in report.field_verdicts],
        )
