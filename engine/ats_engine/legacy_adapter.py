"""Explicit adapter around the uncalibrated v1 lexical/semantic diagnostic."""

from __future__ import annotations

from typing import Any

from .scoring import ats_match_score

ADAPTER_ID = "legacy-diagnostic-v1"
ADAPTER_VERSION = "1.0.0"


def legacy_diagnostic(*args: Any, **kwargs: Any) -> dict[str, Any]:
    """Run the retained diagnostic and label its uncalibrated boundary."""
    result = ats_match_score(*args, **kwargs)
    return {
        **result,
        "adapter_id": ADAPTER_ID,
        "adapter_version": ADAPTER_VERSION,
        "calibration_status": "NOT_RUN",
    }
