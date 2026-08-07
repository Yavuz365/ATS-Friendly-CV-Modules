from __future__ import annotations

from datetime import date

import pytest

from ats_engine.contracts import (
    ApplicationEvent,
    CandidateFact,
    ConsentStatus,
    DataStatus,
    EvidenceConflict,
    EvidenceRecord,
    JobPostingSnapshot,
    JobRequirement,
    ProcessStatus,
    SourceArtifact,
    VerificationStatus,
)
from ats_engine.storage import (
    ConsentRequiredError,
    DuplicateRecordError,
    MissingRecordError,
    PrivacyAction,
    RetentionExpiredError,
    SQLiteContractStore,
    StorageError,
)


def _source(source_id: str) -> SourceArtifact:
    return SourceArtifact(
        id=source_id,
        filename=f"{source_id}.txt",
        media_type="text/plain",
        sha256="b" * 64,
        locator=f"fixture://{source_id}",
        version="1",
    )


def _snapshot() -> JobPostingSnapshot:
    return JobPostingSnapshot(
        id="JOB-1",
        source_artifact_id="SRC-1",
        captured_at="2026-08-06T10:00:00+00:00",
        text_sha256="a" * 64,
        locale="tr-TR",
    )


def _requirement() -> JobRequirement:
    return JobRequirement(
        id="REQ-1",
        job_posting_id="JOB-1",
        text="İleri düzey İngilizce zorunludur.",
        requirement_type="LANGUAGE",
        explicit=True,
        category="LANGUAGE",
        modality="MUST",
        span_start=0,
        span_end=34,
    )


def _fact(*, consent: ConsentStatus, retention_until: str = "2027-01-01") -> CandidateFact:
    return CandidateFact(
        id="FACT-1",
        field="experience.erp",
        value="SAP",
        source_artifact_ids=["SRC-CV-1"],
        data_status=DataStatus.KNOWN,
        verification_status=VerificationStatus.PARTIAL,
        sensitivity="PERSONAL",
        consent_status=consent,
        retention_until=retention_until,
    )


def test_job_snapshots_are_immutable_and_requirement_reviews_are_versioned():
    with SQLiteContractStore() as store:
        store.add_source_artifact(_source("SRC-1"))
        store.add_job_posting(_snapshot())
        with pytest.raises(DuplicateRecordError):
            store.add_job_posting(_snapshot())

        store.add_job_requirement(_requirement())
        first = store.review_requirement(
            "REQ-1",
            approval_version="1",
            reviewer="human@example.test",
            decision=ProcessStatus.PASS,
            reviewed_at="2026-08-06T10:05:00+00:00",
        )
        second = store.review_requirement(
            "REQ-1",
            approval_version="2",
            reviewer="human@example.test",
            decision=ProcessStatus.REVIEW,
            reviewed_at="2026-08-06T10:06:00+00:00",
            notes="Negation requires a second reviewer.",
        )

        assert first.approval_version == "1"
        assert second.approval_version == "2"
        assert [item.approval_version for item in store.requirement_reviews("REQ-1")] == ["1", "2"]
        with pytest.raises(DuplicateRecordError):
            store.review_requirement(
                "REQ-1",
                approval_version="2",
                reviewer="other@example.test",
                decision=ProcessStatus.PASS,
            )


def test_personal_fact_requires_consent_or_redaction():
    with SQLiteContractStore() as store:
        store.add_source_artifact(_source("SRC-CV-1"))
        with pytest.raises(ConsentRequiredError):
            store.add_candidate_fact(_fact(consent=ConsentStatus.NOT_COLLECTED))

        store.add_candidate_fact(_fact(consent=ConsentStatus.GRANTED))
        payload = store.get_candidate_fact("FACT-1")
        assert payload is not None and payload["value"] == "SAP"


def test_retention_and_consent_actions_restrict_read_without_deleting_evidence():
    with SQLiteContractStore() as store:
        store.add_source_artifact(_source("SRC-CV-1"))
        store.add_candidate_fact(_fact(consent=ConsentStatus.GRANTED, retention_until="2026-08-07"))
        store.record_privacy_action(
            PrivacyAction(
                action_id="PA-1",
                entity_kind="candidate_fact",
                entity_id="FACT-1",
                action="CONSENT_REVOKE",
                reason="Candidate revoked consent.",
                actor="candidate",
                occurred_at="2026-08-06T11:00:00+00:00",
            )
        )
        with pytest.raises(RetentionExpiredError):
            store.get_candidate_fact("FACT-1", as_of=date(2026, 8, 6))

        restricted = store.get_candidate_fact("FACT-1", as_of=date(2026, 8, 6), include_restricted=True)
        assert restricted is not None and restricted["value"] is None
        assert restricted["redacted"] is True
        raw = store.get("candidate_fact", "FACT-1")
        assert raw is not None and raw["value"] == "SAP"


def test_evidence_and_conflict_require_existing_fact_and_evidence():
    with SQLiteContractStore() as store:
        store.add_source_artifact(_source("SRC-CV-1"))
        store.add_candidate_fact(_fact(consent=ConsentStatus.GRANTED))
        evidence = EvidenceRecord(
            id="EVD-1",
            candidate_fact_id="FACT-1",
            source_artifact_id="SRC-CV-1",
            locator="experience[0]",
            excerpt="SAP ile sipariş takibi",
        )
        store.add_evidence(evidence)
        store.add_conflict(
            EvidenceConflict(
                id="CONFLICT-1",
                candidate_fact_id="FACT-1",
                evidence_ids=["EVD-1"],
                reason="Aynı sistem için farklı tarih aralıkları mevcut.",
            )
        )
        assert len(store.list_records("evidence_record")) == 1
        assert len(store.list_records("evidence_conflict")) == 1


def test_unobserved_outcome_is_censored_not_automatically_failed():
    with SQLiteContractStore() as store:
        with pytest.raises(StorageError, match="censoring_reason"):
            store.add_application_event(
                ApplicationEvent(
                    id="EVT-1",
                    application_id="APP-1",
                    event_type="OUTCOME_CHECK",
                    occurred_at="2026-08-06T12:00:00+00:00",
                    outcome_observed=False,
                )
            )

        store.add_application_event(
            ApplicationEvent(
                id="EVT-2",
                application_id="APP-1",
                event_type="OUTCOME_CHECK",
                occurred_at="2026-08-06T12:00:00+00:00",
                outcome_observed=False,
                censoring_reason="Employer response window remains open.",
            )
        )
        payload = store.get("application_event", "EVT-2")
        assert payload is not None and payload["outcome_observed"] is False
        assert payload["data_status"] == "KNOWN"


# EVD-002: tested export (data portability) and delete (right to erasure) paths.
def test_export_candidate_fact_bundles_fact_evidence_sources_and_privacy_history():
    with SQLiteContractStore() as store:
        store.add_source_artifact(_source("SRC-CV-1"))
        store.add_candidate_fact(_fact(consent=ConsentStatus.GRANTED))
        store.add_evidence(
            EvidenceRecord(
                id="EV-1",
                candidate_fact_id="FACT-1",
                source_artifact_id="SRC-CV-1",
                locator="line:3",
                excerpt="SAP deneyimi",
            )
        )
        store.record_privacy_action(
            PrivacyAction(
                action_id="PA-EXPORT-1",
                entity_kind="candidate_fact",
                entity_id="FACT-1",
                action="EXPORT",
                reason="Candidate requested a data export.",
                actor="candidate",
                occurred_at="2026-08-07T09:00:00+00:00",
            )
        )

        bundle = store.export_candidate_fact("FACT-1")

        assert bundle["candidate_fact"]["value"] == "SAP"
        assert [e["id"] for e in bundle["evidence"]] == ["EV-1"]
        assert [s["id"] for s in bundle["source_artifacts"]] == ["SRC-CV-1"]
        assert [a["action"] for a in bundle["privacy_actions"]] == ["EXPORT"]
        assert bundle["exported_at"]


def test_export_unknown_fact_raises_missing_record_error():
    with SQLiteContractStore() as store:
        with pytest.raises(MissingRecordError):
            store.export_candidate_fact("does-not-exist")


def test_delete_candidate_fact_irreversibly_erases_value():
    with SQLiteContractStore() as store:
        store.add_source_artifact(_source("SRC-CV-1"))
        store.add_candidate_fact(_fact(consent=ConsentStatus.GRANTED))

        action = store.delete_candidate_fact(
            "FACT-1", actor="candidate", reason="Right to erasure request.", action_id="PA-DELETE-1"
        )
        assert action.action == "DELETE"

        # Even an "include_restricted" read never recovers the erased value —
        # this is a real delete, not a read-time restriction like REDACT.
        payload = store.get_candidate_fact("FACT-1", include_restricted=True)
        assert payload is not None
        assert payload["value"] is None
        assert payload["redacted"] is True
        assert payload["consent_status"] == ConsentStatus.REVOKED.value

        with pytest.raises(RetentionExpiredError):
            store.get_candidate_fact("FACT-1")


def test_delete_requires_actor_and_reason():
    with SQLiteContractStore() as store:
        store.add_source_artifact(_source("SRC-CV-1"))
        store.add_candidate_fact(_fact(consent=ConsentStatus.GRANTED))
        with pytest.raises(StorageError):
            store.delete_candidate_fact("FACT-1", actor="", reason="", action_id="PA-DELETE-2")


def test_storage_module_has_no_network_client_local_first_guarantee():
    import ats_engine.storage as storage_module

    source = storage_module.__file__
    with open(source, encoding="utf-8") as f:
        text = f.read()
    for banned in ("import requests", "import httpx", "import urllib", "import socket", "aiohttp"):
        assert banned not in text, f"storage.py must stay local-first; found forbidden import: {banned}"


def test_storage_errors_never_embed_personal_value_only_ids():
    with SQLiteContractStore() as store:
        store.add_source_artifact(_source("SRC-CV-1"))
        secret_value = "super-secret-personal-detail-should-not-leak"
        store.add_candidate_fact(
            CandidateFact(
                id="FACT-SECRET",
                field="experience.erp",
                value=secret_value,
                source_artifact_ids=["SRC-CV-1"],
                data_status=DataStatus.KNOWN,
                verification_status=VerificationStatus.PARTIAL,
                sensitivity="PERSONAL",
                consent_status=ConsentStatus.GRANTED,
                retention_until="2026-01-01",  # already expired
            )
        )
        with pytest.raises(RetentionExpiredError) as excinfo:
            store.get_candidate_fact("FACT-SECRET")
        assert secret_value not in str(excinfo.value)


# OPS-001: event versions, source, distinct observed/occurred time, and
# event-level privacy/retention enforcement.
def test_application_event_defaults_observed_at_to_occurred_at_when_unset():
    with SQLiteContractStore() as store:
        store.add_application_event(
            ApplicationEvent(
                id="EVT-OBS-1",
                application_id="APP-1",
                event_type="SUBMITTED",
                occurred_at="2026-08-01T09:00:00+00:00",
            )
        )
        payload = store.get_application_event("EVT-OBS-1")
        assert payload is not None
        assert payload["observed_at"] == "2026-08-01T09:00:00+00:00"
        assert payload["event_version"] == 1
        assert payload["source"] == "self-reported"


def test_application_event_keeps_distinct_observed_at_when_reported_late():
    with SQLiteContractStore() as store:
        store.add_application_event(
            ApplicationEvent(
                id="EVT-OBS-2",
                application_id="APP-1",
                event_type="REJECTED",
                occurred_at="2026-08-01T09:00:00+00:00",
                observed_at="2026-08-15T09:00:00+00:00",
                event_version=2,
                source="candidate-self-report",
            )
        )
        payload = store.get_application_event("EVT-OBS-2")
        assert payload["occurred_at"] != payload["observed_at"]
        assert payload["event_version"] == 2
        assert payload["source"] == "candidate-self-report"


def test_application_event_read_respects_retention_and_privacy_actions():
    with SQLiteContractStore() as store:
        store.add_application_event(
            ApplicationEvent(
                id="EVT-PRIV-1",
                application_id="APP-1",
                event_type="INTERVIEW_SCHEDULED",
                occurred_at="2026-08-01T09:00:00+00:00",
                payload={"note": "sensitive scheduling detail"},
            )
        )
        # Unrestricted read still works.
        assert store.get_application_event("EVT-PRIV-1")["payload"] == {"note": "sensitive scheduling detail"}

        store.record_privacy_action(
            PrivacyAction(
                action_id="PA-EVT-1",
                entity_kind="application_event",
                entity_id="EVT-PRIV-1",
                action="REDACT",
                reason="Candidate requested redaction.",
                actor="candidate",
                occurred_at="2026-08-02T09:00:00+00:00",
            )
        )
        with pytest.raises(RetentionExpiredError):
            store.get_application_event("EVT-PRIV-1")

        restricted_payload = store.get_application_event("EVT-PRIV-1", include_restricted=True)
        assert restricted_payload["payload"] == {}
        assert restricted_payload["redacted"] is True
