"""EVAL-002 — Provenance log is append-only, durable and run-scoped."""

from __future__ import annotations

import sqlite3

import pytest

from ats_engine.provenance import (
    ProvenanceKind,
    ProvenanceLog,
    ProvenanceStorageError,
    new_run_id,
)


def test_record_and_list_for_run() -> None:
    log = ProvenanceLog()
    run = new_run_id()
    artifact = log.record(
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
        parent_ids=[artifact.id],
        status="EXACT",
        detail={"term": "incoterms"},
    )
    rows = log.list_for_run(run)
    assert len(rows) == 2
    assert rows[0].kind is ProvenanceKind.ARTIFACT_INGEST
    assert rows[1].parent_ids == (artifact.id,)


def test_duplicate_id_rejected() -> None:
    log = ProvenanceLog()
    run = new_run_id()
    log.record(ProvenanceKind.NOTE, run_id=run, entry_id="prov-fixed", detail={"n": 1})
    with pytest.raises(ValueError):
        log.record(ProvenanceKind.NOTE, run_id=run, entry_id="prov-fixed", detail={"n": 2})


def test_sqlite_reopen_roundtrip_reads_all_entries(tmp_path) -> None:
    db = tmp_path / "prov.sqlite"
    run = "run-reopen"
    with ProvenanceLog(db) as log:
        artifact = log.record(
            ProvenanceKind.ARTIFACT_INGEST,
            run_id=run,
            subject_id="artifact-1",
            status="PASS",
            entry_id="prov-001",
            occurred_at="2026-08-07T00:00:00+00:00",
        )
        match = log.record(
            ProvenanceKind.MATCH_STAGE,
            run_id=run,
            subject_id="req-1",
            parent_ids=[artifact.id],
            status="EXACT",
            detail={"term": "incoterms"},
            entry_id="prov-002",
            occurred_at="2026-08-07T00:00:01+00:00",
        )
        log.record(
            ProvenanceKind.SCREENING_DECISION,
            run_id=run,
            subject_id="candidate-1",
            parent_ids=[match.id],
            status="REVIEW",
            detail={"gate": "G2"},
            entry_id="prov-003",
            occurred_at="2026-08-07T00:00:02+00:00",
        )

    with ProvenanceLog(db) as reopened:
        rows = reopened.list_for_run(run)
        assert [row.id for row in rows] == ["prov-001", "prov-002", "prov-003"]
        assert rows[1].parent_ids == ("prov-001",)
        assert rows[2].detail == {"gate": "G2"}
        assert len(reopened.list_all()) == 3


def test_sqlite_reopen_filters_runs(tmp_path) -> None:
    db = tmp_path / "prov.sqlite"
    with ProvenanceLog(db) as log:
        log.record(ProvenanceKind.NOTE, run_id="run-a", entry_id="prov-a")
        log.record(ProvenanceKind.NOTE, run_id="run-b", entry_id="prov-b")

    with ProvenanceLog(db) as reopened:
        assert [row.id for row in reopened.list_for_run("run-a")] == ["prov-a"]
        assert [row.id for row in reopened.list_for_run("run-b")] == ["prov-b"]


def test_duplicate_id_rejected_after_reopen(tmp_path) -> None:
    db = tmp_path / "prov.sqlite"
    with ProvenanceLog(db) as log:
        log.record(ProvenanceKind.NOTE, run_id="run-a", entry_id="prov-fixed")

    with ProvenanceLog(db) as reopened:
        with pytest.raises(ValueError, match="already exists"):
            reopened.record(ProvenanceKind.NOTE, run_id="run-a", entry_id="prov-fixed")


def test_corrupt_persisted_json_raises_typed_error(tmp_path) -> None:
    db = tmp_path / "prov.sqlite"
    with ProvenanceLog(db) as log:
        log.record(ProvenanceKind.NOTE, run_id="run-a", entry_id="prov-corrupt")

    connection = sqlite3.connect(db)
    connection.execute(
        "UPDATE provenance_entries SET detail_json = ? WHERE id = ?",
        ("not-json", "prov-corrupt"),
    )
    connection.commit()
    connection.close()

    with ProvenanceLog(db) as reopened:
        with pytest.raises(ProvenanceStorageError, match="prov-corrupt"):
            reopened.list_all()


def test_unknown_persisted_kind_raises_typed_error(tmp_path) -> None:
    db = tmp_path / "prov.sqlite"
    with ProvenanceLog(db) as log:
        log.record(ProvenanceKind.NOTE, run_id="run-a", entry_id="prov-kind")

    connection = sqlite3.connect(db)
    connection.execute(
        "UPDATE provenance_entries SET kind = ? WHERE id = ?",
        ("UNKNOWN_KIND", "prov-kind"),
    )
    connection.commit()
    connection.close()

    with ProvenanceLog(db) as reopened:
        with pytest.raises(ProvenanceStorageError, match="prov-kind"):
            reopened.list_all()


def test_to_jsonable_is_serializable() -> None:
    log = ProvenanceLog()
    run = new_run_id()
    log.record(ProvenanceKind.EVALUATION_RUN, run_id=run, status="STARTED")
    payload = log.to_jsonable(run)
    assert payload[0]["kind"] == "EVALUATION_RUN"
    assert isinstance(payload[0]["parent_ids"], list)
