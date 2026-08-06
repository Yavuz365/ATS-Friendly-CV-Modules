"""Feature-flagged, version-pinned ESCO ontology adapter (MAT-003).

This module intentionally does **not** ship a full ESCO dump or network calls.
It provides a safe, revision-pinned adapter skeleton that:

* is disabled by default (feature flag OFF → NOT_RUN / abstain),
* never produces a final PASS / verified match,
* only returns review-required candidate signals when explicitly enabled,
* rejects floating revisions ("latest", "main", etc.).

ESCO reference: European Skills, Competences, Qualifications and Occupations
v1.2.1 (December 2025 pin target). Real concept mapping and data loading
remain future work; this file only establishes the contract boundary.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .matching import AdapterResult, AdapterStatus, VersionedMatchAdapter

# Canonical pin for this research prototype. Do not change without a new
# adapter_version + revision and an evaluation card update.
ESCO_VERSION = "1.2.1"
ESCO_REVISION = "2025-12-esco-v1.2.1-pin"
ADAPTER_ID = "esco-ontology"


@dataclass(frozen=True)
class EscoAdapterConfig:
    """Runtime configuration for the ESCO adapter."""

    enabled: bool = False  # feature flag — OFF by default
    version: str = ESCO_VERSION
    revision: str = ESCO_REVISION
    locale: str = "en"  # ESCO primary; TR mapping is future work
    domain: str = "general"


def _abstain_matcher(_term: str, _text: str) -> AdapterResult:
    """Default behaviour when the feature flag is off or data is unavailable."""
    return AdapterResult(
        status=AdapterStatus.NOT_RUN,
        explanation=(
            "ESCO adapter is disabled or data is not loaded; "
            "ontology stage abstains (NOT_RUN)."
        ),
    )


def _disabled_or_missing_data_matcher(_term: str, _text: str) -> AdapterResult:
    """Used when the flag is on but no concept store has been loaded yet."""
    return AdapterResult(
        status=AdapterStatus.NOT_RUN,
        explanation=(
            "ESCO adapter enabled but concept store is empty; "
            "ontology stage abstains until a pinned dump is loaded."
        ),
    )


def build_esco_adapter(
    config: EscoAdapterConfig | None = None,
    concept_matcher: Callable[[str, str], AdapterResult] | None = None,
) -> VersionedMatchAdapter | None:
    """Build a VersionedMatchAdapter for the ontology cascade stage.

    Returns ``None`` when the feature flag is off so that the matching cascade
    simply skips the ontology stage (clean abstain).

    When enabled, a real ``concept_matcher`` may be supplied. If it is omitted,
    the adapter still runs but returns NOT_RUN (no silent false matches).
    """
    cfg = config or EscoAdapterConfig()
    if not cfg.enabled:
        return None

    matcher = concept_matcher or _disabled_or_missing_data_matcher

    return VersionedMatchAdapter(
        adapter_id=ADAPTER_ID,
        version=cfg.version,
        revision=cfg.revision,
        matcher=matcher,
        locale=cfg.locale,
        domain=cfg.domain,
    )


def esco_adapter_status(config: EscoAdapterConfig | None = None) -> dict[str, str | bool]:
    """Machine-readable status for diagnostics and evaluation cards."""
    cfg = config or EscoAdapterConfig()
    return {
        "adapter_id": ADAPTER_ID,
        "version": cfg.version,
        "revision": cfg.revision,
        "enabled": cfg.enabled,
        "default_behaviour": "NOT_RUN / abstain",
        "produces_verified_pass": False,
        "review_required_on_match": True,
    }
