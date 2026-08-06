"""Allowlisted, evidence-bound synthesis changes."""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import replace
from datetime import datetime, timezone

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

PROTECTED_SEGMENTS = frozenset(
    {"name", "employer", "company", "title", "start_date", "end_date", "date", "degree", "language_level", "metric"}
)

_UNTRUSTED_INSTRUCTION_SIGNALS = (
    re.compile(r"\bignore (?:all|any|the|previous) (?:rules|instructions)\b", re.I),
    re.compile(r"\bsystem prompt\b", re.I),
    re.compile(r"\bdeveloper message\b", re.I),
    re.compile(r"\bexecute (?:this|the following)\b", re.I),
)


def inspect_untrusted_text(text: str) -> dict:
    """Classify embedded instructions as data and surface review signals."""
    signals = [pattern.pattern for pattern in _UNTRUSTED_INSTRUCTION_SIGNALS if pattern.search(text or "")]
    return {
        "status": ProcessStatus.REVIEW.value if signals else ProcessStatus.PASS.value,
        "signals": signals,
        "execution_allowed": False,
        "instruction_boundary": "UNTRUSTED_DOCUMENT_DATA",
    }


def _path_allowed(path: str) -> bool:
    return any(
        path == prefix or path.startswith(prefix + ".") or path.startswith(prefix + "[")
        for prefix in ALLOWLISTED_PATH_PREFIXES
    )


def _protected_path(path: str) -> bool:
    if path in PROTECTED_PATHS:
        return True
    segments = {part for part in re.split(r"[.\[\]]+", path) if part and not part.isdigit()}
    return bool(segments & PROTECTED_SEGMENTS)


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
        if _protected_path(path):
            raise InvalidInputError(f"Korunan aday alanı değiştirilemez: {path}", field=f"proposals[{index}].path")
        if not _path_allowed(path):
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
    return replace(change_set, status=ProcessStatus.PASS, human_approved=True, decision_reason="Human approved")


def reject_change_set(change_set: SynthesisChangeSet, reason: str) -> SynthesisChangeSet:
    """Record an explicit rejection without deleting the proposal."""
    if not reason.strip():
        raise InvalidInputError("Ret gerekçesi zorunludur.", field="reason")
    return replace(change_set, status=ProcessStatus.FAIL, human_approved=False, decision_reason=reason.strip())


def apply_change_set(
    change_set: SynthesisChangeSet, document: dict[str, str]
) -> tuple[dict[str, str], SynthesisChangeSet]:
    """Apply an approved set to a path-keyed document and retain its parent values."""
    if change_set.status is not ProcessStatus.PASS or not change_set.human_approved:
        raise InvalidInputError("Yalnız açıkça onaylanmış ChangeSet uygulanabilir.", field="change_set.status")
    updated = dict(document)
    for change in change_set.changes:
        current = updated.get(change.path, "")
        if current != change.old_value:
            raise InvalidInputError(
                f"Eşzamanlı değişiklik tespit edildi: {change.path}",
                field=change.path,
            )
        updated[change.path] = change.new_value
    applied = replace(change_set, applied_at=datetime.now(timezone.utc).isoformat())
    return updated, applied


def rollback_change_set(
    applied_change_set: SynthesisChangeSet,
    document: dict[str, str],
    *,
    rollback_id: str,
) -> tuple[dict[str, str], SynthesisChangeSet]:
    """Create and apply a reversible, auditable inverse ChangeSet."""
    if not applied_change_set.applied_at:
        raise InvalidInputError("Uygulanmamış ChangeSet geri alınamaz.", field="applied_at")
    inverse = SynthesisChangeSet(
        id=rollback_id,
        changes=[
            SynthesisChange(
                path=change.path,
                old_value=change.new_value,
                new_value=change.old_value,
                evidence_ids=change.evidence_ids,
                reason=f"Rollback of {applied_change_set.id}",
            )
            for change in applied_change_set.changes
        ],
        status=ProcessStatus.PASS,
        human_approved=True,
        parent_id=applied_change_set.id,
        decision_reason="Human-approved rollback",
        rolled_back_from=applied_change_set.id,
    )
    return apply_change_set(inverse, document)
