from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

from ats_engine import parse_document
from ats_engine.errors import DocumentParseError


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
            continue

        result = parse_document(path)
        assert result.status.value == fixture["expected_status"]
        assert result.extraction_method in fixture["expected_extraction_methods"]
        for expected_text in fixture["required_text"]:
            assert expected_text in result.text
        for key, expected in fixture.get("structural_features", {}).items():
            assert result.structural_features[key] == expected
