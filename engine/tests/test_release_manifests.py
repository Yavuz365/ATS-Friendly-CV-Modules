from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_validator(root: Path):
    path = root / "scripts" / "validate_release_manifests.py"
    spec = importlib.util.spec_from_file_location("release_manifest_validator", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_alpha_release_manifests_are_commit_pinned_and_non_production():
    root = Path(__file__).parents[2]
    validator = _load_validator(root)
    manifests = sorted((root / "docs" / "releases").glob("2.0.0-alpha.*.json"))
    assert [path.name for path in manifests] == ["2.0.0-alpha.1.json", "2.0.0-alpha.2.json"]
    errors = []
    for path in manifests:
        errors.extend(validator.validate_manifest(path, repo=root))
    assert errors == []
