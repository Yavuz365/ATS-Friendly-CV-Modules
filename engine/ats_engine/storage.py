"""Append-only SQLite persistence for evidence-first contracts.

The store deliberately keeps source records immutable. Human approvals and privacy
operations are separate append-only records so that the original evidence trail is
never silently rewritten.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from .contracts import (
    ApplicationEvent,
    CandidateFact,
    ConsentStatus,
    EvidenceConflict,
    EvidenceRecord,
    JobPostingSnapshot,
    JobRequirement,
    ProcessStatus,
    to_primitive,
)


class StorageError(RuntimeError):
    """Base persistence error."""


class DuplicateRecordError(StorageError):
    """Raised when an immutable identifier is written twice."""


class MissingRecordError(StorageError):
    """Raised when a referenced record does not exist."""


class ConsentRequiredError(StorageError):
    """Raised when personal data would be persisted without explicit consent."""


class RetentionExpiredError(StorageError):
    """Raised when a retained personal fact is no longer readable."""


@dataclass(frozen=True)
class RequirementApproval:
    requirement_id: str
    approval_version: str
    reviewer: str
    decision: ProcessStatus
    reviewed_at: str
    notes: str = ""


@dataclass(frozen=True)
class PrivacyAction:
    action_id: str
    entity_kind: str
    entity_id: str
    action: str
    reason: str
    actor: str
    occurred_at: str


_KIND_BY_TYPE: dict[type[Any], str] = {
    JobPostingSnapshot: "job_posting_snapshot",
    JobRequirement: "job_requirement",
    CandidateFact: "candidate_fact",
    EvidenceRecord: "evidence_record",
    EvidenceConflict: "evidence_conflict",
    ApplicationEvent: "application_event",
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _json_payload(value: Any) -> str:
    return json.dumps(to_primitive(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _iso_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise StorageError(f"Geçersiz ISO tarih: {value}") from exc


class SQLiteContractStore:
    """Small append-only store for contract records.

    ``:memory:`` is useful for tests. File-backed databases create their parent
    directory automatically. Records are JSON snapshots keyed by contract kind and
    immutable id; review and privacy actions live in independent ledgers.
    """

    def __init__(self, path: str | Path = ":memory:") -> None:
        self.path = str(path)
        if self.path != ":memory:":
            Path(self.path).expanduser().resolve().parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        self._migrate()

    def close(self) -> None:
        self.connection.close()

    def __enter__(self) -> SQLiteContractStore:
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.close()

    def _migrate(self) -> None:
        self.connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS contract_records (
                kind TEXT NOT NULL,
                record_id TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                PRIMARY KEY (kind, record_id)
            );

            CREATE TABLE IF NOT EXISTS requirement_reviews (
                requirement_id TEXT NOT NULL,
                approval_version TEXT NOT NULL,
                reviewer TEXT NOT NULL,
                decision TEXT NOT NULL,
                reviewed_at TEXT NOT NULL,
                notes TEXT NOT NULL,
                requirement_snapshot_json TEXT NOT NULL,
                PRIMARY KEY (requirement_id, approval_version)
            );

            CREATE TABLE IF NOT EXISTS privacy_actions (
                action_id TEXT PRIMARY KEY,
                entity_kind TEXT NOT NULL,
                entity_id TEXT NOT NULL,
                action TEXT NOT NULL,
                reason TEXT NOT NULL,
                actor TEXT NOT NULL,
                occurred_at TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_contract_records_kind
                ON contract_records(kind);
            CREATE INDEX IF NOT EXISTS idx_privacy_entity
                ON privacy_actions(entity_kind, entity_id, occurred_at);
            """
        )
        self.connection.commit()

    def append(self, record: Any) -> None:
        kind = _KIND_BY_TYPE.get(type(record))
        if kind is None:
            raise StorageError(f"Desteklenmeyen contract tipi: {type(record).__name__}")
        record_id = getattr(record, "id", "")
        if not record_id:
            raise StorageError("Contract id zorunludur.")
        self._validate_before_append(record)
        try:
            with self.connection:
                self.connection.execute(
                    "INSERT INTO contract_records(kind, record_id, payload_json, created_at) VALUES (?, ?, ?, ?)",
                    (kind, record_id, _json_payload(record), _utc_now()),
                )
        except sqlite3.IntegrityError as exc:
            raise DuplicateRecordError(f"Immutable kayıt zaten var: {kind}/{record_id}") from exc

    def _validate_before_append(self, record: Any) -> None:
        if isinstance(record, JobRequirement):
            self._require_record("job_posting_snapshot", record.job_posting_id)
        elif isinstance(record, CandidateFact):
            if (
                record.sensitivity.upper() != "PUBLIC"
                and record.consent_status is not ConsentStatus.GRANTED
                and not record.redacted
            ):
                raise ConsentRequiredError(
                    "Kişisel CandidateFact yalnız GRANTED consent veya redacted değerle saklanabilir."
                )
        elif isinstance(record, EvidenceRecord):
            self._require_record("candidate_fact", record.candidate_fact_id)
        elif isinstance(record, EvidenceConflict):
            self._require_record("candidate_fact", record.candidate_fact_id)
            for evidence_id in record.evidence_ids:
                self._require_record("evidence_record", evidence_id)
        elif isinstance(record, ApplicationEvent):
            if record.outcome_observed is False and not record.censoring_reason:
                raise StorageError(
                    "outcome_observed=False olduğunda censoring_reason zorunludur; gözlenmeyen sonuç başarısızlık değildir."
                )

    def _require_record(self, kind: str, record_id: str) -> dict[str, Any]:
        record = self.get(kind, record_id)
        if record is None:
            raise MissingRecordError(f"Referans kayıt bulunamadı: {kind}/{record_id}")
        return record

    def get(self, kind: str, record_id: str) -> dict[str, Any] | None:
        row = self.connection.execute(
            "SELECT payload_json FROM contract_records WHERE kind = ? AND record_id = ?",
            (kind, record_id),
        ).fetchone()
        if row is None:
            return None
        return json.loads(str(row["payload_json"]))

    def list_records(self, kind: str) -> list[dict[str, Any]]:
        rows = self.connection.execute(
            "SELECT payload_json FROM contract_records WHERE kind = ? ORDER BY created_at, record_id",
            (kind,),
        ).fetchall()
        return [json.loads(str(row["payload_json"])) for row in rows]

    def add_job_posting(self, snapshot: JobPostingSnapshot) -> None:
        self.append(snapshot)

    def add_job_requirement(self, requirement: JobRequirement) -> None:
        self.append(requirement)

    def add_candidate_fact(self, fact: CandidateFact) -> None:
        self.append(fact)

    def add_evidence(self, evidence: EvidenceRecord) -> None:
        self.append(evidence)

    def add_conflict(self, conflict: EvidenceConflict) -> None:
        self.append(conflict)

    def add_application_event(self, event: ApplicationEvent) -> None:
        self.append(event)

    def review_requirement(
        self,
        requirement_id: str,
        *,
        approval_version: str,
        reviewer: str,
        decision: ProcessStatus,
        reviewed_at: str | None = None,
        notes: str = "",
    ) -> RequirementApproval:
        if decision not in {ProcessStatus.PASS, ProcessStatus.FAIL, ProcessStatus.REVIEW}:
            raise StorageError("Requirement review kararı PASS, FAIL veya REVIEW olmalıdır.")
        if not approval_version or not reviewer:
            raise StorageError("approval_version ve reviewer zorunludur.")
        requirement = self._require_record("job_requirement", requirement_id)
        approval = RequirementApproval(
            requirement_id=requirement_id,
            approval_version=approval_version,
            reviewer=reviewer,
            decision=decision,
            reviewed_at=reviewed_at or _utc_now(),
            notes=notes,
        )
        try:
            with self.connection:
                self.connection.execute(
                    """
                    INSERT INTO requirement_reviews(
                        requirement_id, approval_version, reviewer, decision,
                        reviewed_at, notes, requirement_snapshot_json
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        approval.requirement_id,
                        approval.approval_version,
                        approval.reviewer,
                        approval.decision.value,
                        approval.reviewed_at,
                        approval.notes,
                        json.dumps(requirement, ensure_ascii=False, sort_keys=True),
                    ),
                )
        except sqlite3.IntegrityError as exc:
            raise DuplicateRecordError(
                f"Requirement approval version zaten var: {requirement_id}/{approval_version}"
            ) from exc
        return approval

    def requirement_reviews(self, requirement_id: str) -> list[RequirementApproval]:
        rows = self.connection.execute(
            """
            SELECT requirement_id, approval_version, reviewer, decision, reviewed_at, notes
            FROM requirement_reviews WHERE requirement_id = ?
            ORDER BY reviewed_at, approval_version
            """,
            (requirement_id,),
        ).fetchall()
        return [
            RequirementApproval(
                requirement_id=str(row["requirement_id"]),
                approval_version=str(row["approval_version"]),
                reviewer=str(row["reviewer"]),
                decision=ProcessStatus(str(row["decision"])),
                reviewed_at=str(row["reviewed_at"]),
                notes=str(row["notes"]),
            )
            for row in rows
        ]

    def record_privacy_action(self, action: PrivacyAction) -> None:
        if action.action not in {"REDACT", "RETENTION_EXPIRE", "CONSENT_REVOKE"}:
            raise StorageError("Desteklenmeyen privacy action.")
        self._require_record(action.entity_kind, action.entity_id)
        try:
            with self.connection:
                self.connection.execute(
                    """
                    INSERT INTO privacy_actions(
                        action_id, entity_kind, entity_id, action, reason, actor, occurred_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        action.action_id,
                        action.entity_kind,
                        action.entity_id,
                        action.action,
                        action.reason,
                        action.actor,
                        action.occurred_at,
                    ),
                )
        except sqlite3.IntegrityError as exc:
            raise DuplicateRecordError(f"Privacy action zaten var: {action.action_id}") from exc

    def get_candidate_fact(
        self,
        fact_id: str,
        *,
        as_of: date | None = None,
        include_restricted: bool = False,
    ) -> dict[str, Any] | None:
        payload = self.get("candidate_fact", fact_id)
        if payload is None:
            return None
        actions = self.connection.execute(
            """
            SELECT action FROM privacy_actions
            WHERE entity_kind = 'candidate_fact' AND entity_id = ?
            ORDER BY occurred_at
            """,
            (fact_id,),
        ).fetchall()
        restricted = any(
            str(row["action"]) in {"REDACT", "RETENTION_EXPIRE", "CONSENT_REVOKE"} for row in actions
        )
        retention_until = payload.get("retention_until")
        if retention_until and _iso_date(str(retention_until)) < (as_of or date.today()):
            restricted = True
        if restricted and not include_restricted:
            raise RetentionExpiredError(f"CandidateFact erişimi privacy/retention nedeniyle kapalı: {fact_id}")
        if restricted:
            payload = dict(payload)
            payload["value"] = None
            payload["redacted"] = True
        return payload
