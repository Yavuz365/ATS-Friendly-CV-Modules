"""EVAL-002 — Provenance log is append-only and run-scoped."""

from __future__ import annotations

import pytest

from ats_engine.provenance import (
    ProvenanceKind,
    ProvenanceLog,
    new_run_id,
)


def test_record_and_list_for_run() -> None:
    log = ProvenanceLog()
    run = new_run_id()
    a = log.record(
        ProvenanceKind.ARTIFACT_INGEST,
        run_id=run,
        subject_id="artifact-1",
        status="PASS",
        detail={"media_type": "application/pdf"},
    )
    log.record(
        ProvenanceKind.MATCH_STAGE,
        run_id=run,
        subject_id="req-1",
        parent_ids=[a.id],
        status="EXACT",
        detail={"term": "incoterms"},
    )
    rows = log.list_for_run(run)
    assert len(rows) == 2
    assert rows[0].kind is ProvenanceKind.ARTIFACT_INGEST
    assert rows[1].parent_ids == (a.id,)


def test_duplicate_id_rejected() -> None:
    log = ProvenanceLog()
    run = new_run_id()
    log.record(ProvenanceKind.NOTE, run_id=run, entry_id="prov-fixed", detail={"n": 1})
    with pytest.raises(ValueError):
        log.record(ProvenanceKind.NOTE, run_id=run, entry_id="prov-fixed", detail={"n": 2})


def test_sqlite_durable_roundtrip(tmp_path) -> None:
    db = tmp_path / "prov.sqlite"
    run = new_run_id()
    with ProvenanceLog(db) as log:
        log.record(
            ProvenanceKind.SCREENING_DECISION,
            run_id=run,
            subject_id="cand-1",
            status="REVIEW",
            detail={"gate": "G2"},
        )
        assert len(log.list_for_run(run)) == 1


def test_to_jsonable_is_serializable() -> None:
    log = ProvenanceLog()
    run = new_run_id()
    log.record(ProvenanceKind.EVALUATION_RUN, run_id=run, status="STARTED")
    payload = log.to_jsonable(run)
    assert payload[0]["kind"] == "EVALUATION_RUN"
    assert isinstance(payload[0]["parent_ids"], list)
