"""Feature-flagged, version-pinned ESCO ontology adapter (MAT-003).

Safe defaults:
* feature flag OFF → returns None (cascade skips ontology stage)
* when enabled, loads a tiny offline micro-subset (not full ESCO)
* matches are always review-required; never a final PASS/verified verdict
* floating revisions ("latest", "main", …) are rejected by VersionedMatchAdapter

ESCO reference pin: v1.2.1 (December 2025 research target).
"""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from functools import lru_cache
from importlib import resources
from typing import Any

from .matching import AdapterResult, AdapterStatus, VersionedMatchAdapter, count_boundary_occurrences
from .text import tr_lower

ESCO_VERSION = "1.2.1"
ESCO_REVISION = "2025-12-esco-v1.2.1-pin"
ADAPTER_ID = "esco-ontology"
_MICRO_RESOURCE = "esco_micro_v1_2_1.json"


@dataclass(frozen=True)
class EscoAdapterConfig:
    enabled: bool = False
    version: str = ESCO_VERSION
    revision: str = ESCO_REVISION
    locale: str = "en"
    domain: str = "general"


@lru_cache(maxsize=1)
def _load_micro_concepts() -> list[dict[str, Any]]:
    """Load the pinned offline micro subset shipped with the package."""
    try:
        root = resources.files("ats_engine")
        data_path = root.joinpath("data", _MICRO_RESOURCE)
        with data_path.open("r", encoding="utf-8") as fh:
            payload = json.load(fh)
    except (FileNotFoundError, OSError, json.JSONDecodeError, TypeError, AttributeError):
        return []
    if payload.get("revision") != ESCO_REVISION:
        # Refuse to use a file whose revision does not match the adapter pin.
        return []
    concepts = payload.get("concepts") or []
    return concepts if isinstance(concepts, list) else []


def _concept_labels(concept: dict[str, Any]) -> list[str]:
    labels: list[str] = []
    for key in ("preferred_label_en", "preferred_label_tr"):
        value = concept.get(key)
        if isinstance(value, str) and value.strip():
            labels.append(tr_lower(value).strip())
    for alt in concept.get("alt_labels") or []:
        if isinstance(alt, str) and alt.strip():
            labels.append(tr_lower(alt).strip())
    # de-dupe while preserving order
    return list(dict.fromkeys(labels))


def _build_micro_matcher() -> Callable[[str, str], AdapterResult]:
    concepts = _load_micro_concepts()

    def matcher(term: str, text: str) -> AdapterResult:
        if not concepts:
            return AdapterResult(
                status=AdapterStatus.NOT_RUN,
                explanation="ESCO micro concept store empty or revision mismatch; ontology abstains.",
            )
        normalized_term = tr_lower(term).strip()
        if not normalized_term:
            return AdapterResult(status=AdapterStatus.NO_MATCH, explanation="Empty term.")

        for concept in concepts:
            labels = _concept_labels(concept)
            # Term itself must be one of the concept labels (ontology lookup),
            # then that label (or an alt) must appear in the text with boundaries.
            if normalized_term not in labels:
                continue
            for label in labels:
                if count_boundary_occurrences(label, text) > 0:
                    uri = concept.get("uri", "")
                    return AdapterResult(
                        status=AdapterStatus.MATCH,
                        matched_variant=label,
                        confidence=0.55,
                        explanation=(
                            f"ESCO micro-subset candidate ({uri}); ontology signal only — human review required."
                        ),
                    )
        return AdapterResult(
            status=AdapterStatus.NO_MATCH,
            explanation="No ESCO micro-subset concept matched with boundary evidence.",
        )

    return matcher


def build_esco_adapter(
    config: EscoAdapterConfig | None = None,
    concept_matcher: Callable[[str, str], AdapterResult] | None = None,
) -> VersionedMatchAdapter | None:
    """Build ontology-stage adapter.

    * flag OFF → ``None`` (cascade skips stage cleanly)
    * flag ON  → VersionedMatchAdapter using micro subset (or injected matcher)
    """
    cfg = config or EscoAdapterConfig()
    if not cfg.enabled:
        return None

    matcher = concept_matcher or _build_micro_matcher()
    return VersionedMatchAdapter(
        adapter_id=ADAPTER_ID,
        version=cfg.version,
        revision=cfg.revision,
        matcher=matcher,
        locale=cfg.locale,
        domain=cfg.domain,
    )


def esco_adapter_status(config: EscoAdapterConfig | None = None) -> dict[str, str | bool | int]:
    cfg = config or EscoAdapterConfig()
    concepts = _load_micro_concepts() if cfg.enabled else []
    return {
        "adapter_id": ADAPTER_ID,
        "version": cfg.version,
        "revision": cfg.revision,
        "enabled": cfg.enabled,
        "concept_count": len(concepts) if cfg.enabled else 0,
        "default_behaviour": "NOT_RUN / abstain",
        "produces_verified_pass": False,
        "review_required_on_match": True,
    }
