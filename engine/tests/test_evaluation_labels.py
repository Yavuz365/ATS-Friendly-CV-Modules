from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_validator(root: Path):
    path = root / "scripts" / "validate_evaluation_labels.py"
    spec = importlib.util.spec_from_file_location("evaluation_label_validator", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_repaired_evaluation_labels_are_reviewed_and_non_promoting():
    root = Path(__file__).parents[2]
    validator = _load_validator(root)
    labels = root / "evaluation" / "gold" / "labels.json"
    assert validator.validate_labels(labels) == []
