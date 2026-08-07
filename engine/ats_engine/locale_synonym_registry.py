"""MAT-002: load and conflict-audit the accepted reviewed-synonym dataset.

``matching.match_term()``'s ``reviewed_synonyms``/``synonym_revision`` gave the
SYNONYM stage a revision-hashed *interface*, but there was no actual accepted,
versioned dataset behind it, and no test that the dataset itself is internally
consistent. This module loads
``evaluation/gold/reviewed_locale_synonyms_tr_en.json`` — a small, reviewed
TR/EN dictionary that records both accepted pairs and explicitly *rejected*
candidate pairs with a reason (abstention evidence) — and audits it for
conflicts before it is used.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .text import tr_lower


def load_reviewed_locale_synonyms(path: str | Path) -> dict[str, Any]:
    """Load the raw reviewed-synonym dataset (accepted + abstained sections)."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if "accepted" not in data or "abstained" not in data:
        raise ValueError("Reviewed synonym dataset 'accepted' ve 'abstained' bölümlerini içermelidir.")
    return data


def accepted_synonyms(dataset: dict[str, Any]) -> dict[str, list[str]]:
    """Return the ``{key: [variants]}`` mapping consumable by ``match_term(reviewed_synonyms=...)``."""
    return {key: list(variants) for key, variants in dataset["accepted"].items()}


def audit_reviewed_synonym_conflicts(accepted: dict[str, list[str]]) -> list[str]:
    """Return a list of conflict descriptions, empty when the dataset is consistent.

    A conflict is any variant string that appears under two *different*
    canonical keys (which would make ``reviewed_synonyms`` ambiguous about
    which key a CV mention should support), or a key that is also listed as
    someone else's variant.
    """
    conflicts: list[str] = []
    variant_owner: dict[str, str] = {}
    normalized_keys = {tr_lower(key).strip() for key in accepted}

    for key, variants in accepted.items():
        norm_key = tr_lower(key).strip()
        for variant in variants:
            norm_variant = tr_lower(variant).strip()
            if norm_variant in normalized_keys and norm_variant != norm_key:
                conflicts.append(f"'{variant}' hem '{key}' değişkeni hem de kendi başına kanonik anahtar.")
            owner = variant_owner.get(norm_variant)
            if owner is not None and owner != norm_key:
                conflicts.append(f"'{variant}' hem '{owner}' hem de '{key}' altında listelenmiş (çakışma).")
            else:
                variant_owner[norm_variant] = norm_key
    return conflicts
