"""Allowlisted, evidence-bound synthesis changes."""

from __future__ import annotations

from collections.abc import Iterable

from .contracts import ProcessStatus, SynthesisChange, SynthesisChangeSet
from .errors import InvalidInputError

PROTECTED_PATHS = frozenset(
    {
        "candidate.name",
        "candidate.employer",
        "candidate.title",
        "candidate.start_date",
        "candidate.end_date",
        "candidate.degree",
        "candidate.language_level",
        "candidate.metric",
    }
)

ALLOWLISTED_PATH_PREFIXES = (
    "cv.summary",
    "cv.experience",
    "cv.skills",
    "cv.education",
    "cv.certifications",
)


def build_change_set(
    change_set_id: str,
    proposals: Iterable[dict],
    *,
    known_evidence_ids: set[str],
) -> SynthesisChangeSet:
    """Validate proposed text changes; reject protected or unsupported mutations."""
    changes: list[SynthesisChange] = []
    for index, proposal in enumerate(proposals):
        path = str(proposal.get("path", ""))
        if path in PROTECTED_PATHS:
            raise InvalidInputError(f"Korunan aday alanı değiştirilemez: {path}", field=f"proposals[{index}].path")
        if not path.startswith(ALLOWLISTED_PATH_PREFIXES):
            raise InvalidInputError(f"Sentez yolu allowlist dışında: {path}", field=f"proposals[{index}].path")
        evidence_ids = list(proposal.get("evidence_ids") or [])
        if not evidence_ids:
            raise InvalidInputError(
                "Her sentez değişikliği en az bir evidence ID taşımalıdır.", field=f"proposals[{index}].evidence_ids"
            )
        unknown = sorted(set(evidence_ids) - known_evidence_ids)
        if unknown:
            raise InvalidInputError(
                "Bilinmeyen evidence ID: " + ", ".join(unknown),
                field=f"proposals[{index}].evidence_ids",
            )
        old_value = str(proposal.get("old_value", ""))
        new_value = str(proposal.get("new_value", ""))
        if not new_value.strip():
            raise InvalidInputError("Yeni değer boş olamaz.", field=f"proposals[{index}].new_value")
        changes.append(
            SynthesisChange(
                path=path,
                old_value=old_value,
                new_value=new_value,
                evidence_ids=evidence_ids,
                reason=str(proposal.get("reason", "evidence-bound revision")),
            )
        )
    return SynthesisChangeSet(
        id=change_set_id,
        changes=changes,
        status=ProcessStatus.REVIEW,
        human_approved=False,
    )


def approve_change_set(change_set: SynthesisChangeSet) -> SynthesisChangeSet:
    """Record the explicit human approval required before applying a change set."""
    return SynthesisChangeSet(
        id=change_set.id,
        changes=change_set.changes,
        status=ProcessStatus.PASS,
        human_approved=True,
        contract_version=change_set.contract_version,
    )
