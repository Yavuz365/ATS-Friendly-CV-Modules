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
    VerificationStatus,
)
from ats_engine.storage import (
    ConsentRequiredError,
    DuplicateRecordError,
    PrivacyAction,
    RetentionExpiredError,
    SQLiteContractStore,
    StorageError,
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
        with pytest.raises(ConsentRequiredError):
            store.add_candidate_fact(_fact(consent=ConsentStatus.NOT_COLLECTED))

        store.add_candidate_fact(_fact(consent=ConsentStatus.GRANTED))
        assert store.get_candidate_fact("FACT-1")["value"] == "SAP"


def test_retention_and_consent_actions_restrict_read_without_deleting_evidence():
    with SQLiteContractStore() as store:
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

        restricted = store.get_candidate_fact(
            "FACT-1", as_of=date(2026, 8, 6), include_restricted=True
        )
        assert restricted["value"] is None
        assert restricted["redacted"] is True
        assert store.get("candidate_fact", "FACT-1")["value"] == "SAP"


def test_evidence_and_conflict_require_existing_fact_and_evidence():
    with SQLiteContractStore() as store:
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
        assert payload["outcome_observed"] is False
        assert payload["data_status"] == "KNOWN"
