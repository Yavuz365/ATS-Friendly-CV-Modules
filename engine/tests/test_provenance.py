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


# ---------------------------------------------------------------------------
# EVAL-002 — SQLite reopen / persistence tests
# ---------------------------------------------------------------------------


def test_sqlite_reopen_returns_all_entries(tmp_path) -> None:
    """Entries written in one session must be visible after reopening the DB."""
    db = tmp_path / "prov.sqlite"
    run = new_run_id()

    # Session 1: write three entries
    with ProvenanceLog(db) as log1:
        a = log1.record(ProvenanceKind.ARTIFACT_INGEST, run_id=run, subject_id="art-1", status="PASS")
        b = log1.record(ProvenanceKind.MATCH_STAGE, run_id=run, subject_id="req-1", parent_ids=[a.id])
        log1.record(ProvenanceKind.SCREENING_DECISION, run_id=run, status="REVIEW", parent_ids=[b.id])

    # Session 2: reopen the same path
    with ProvenanceLog(db) as log2:
        all_entries = log2.list_all()
        assert len(all_entries) == 3
        kinds = [e.kind for e in all_entries]
        assert ProvenanceKind.ARTIFACT_INGEST in kinds
        assert ProvenanceKind.MATCH_STAGE in kinds
        assert ProvenanceKind.SCREENING_DECISION in kinds

        # Ordering: occurred_at ascending
        assert all_entries[0].kind is ProvenanceKind.ARTIFACT_INGEST

        # run filtering
        run_entries = log2.list_for_run(run)
        assert len(run_entries) == 3
        other_run_entries = log2.list_for_run("run-does-not-exist")
        assert other_run_entries == []


def test_sqlite_reopen_parent_ids_reconstructed(tmp_path) -> None:
    """Parent-ID tuples must survive a database close/reopen cycle."""
    db = tmp_path / "prov.sqlite"
    run = new_run_id()

    with ProvenanceLog(db) as log1:
        a = log1.record(ProvenanceKind.ARTIFACT_INGEST, run_id=run)
        b = log1.record(ProvenanceKind.MATCH_STAGE, run_id=run, parent_ids=[a.id])

    with ProvenanceLog(db) as log2:
        entries = log2.list_for_run(run)
        match_entry = next(e for e in entries if e.kind is ProvenanceKind.MATCH_STAGE)
        assert match_entry.parent_ids == (a.id,)
        assert isinstance(match_entry.parent_ids, tuple)


def test_sqlite_reopen_detail_dict_reconstructed(tmp_path) -> None:
    """Detail dicts must survive a database close/reopen cycle."""
    db = tmp_path / "prov.sqlite"
    run = new_run_id()
    detail = {"gate": "G2", "score": 0.85, "flags": ["review"]}

    with ProvenanceLog(db) as log1:
        log1.record(ProvenanceKind.SCREENING_DECISION, run_id=run, detail=detail)

    with ProvenanceLog(db) as log2:
        entries = log2.list_all()
        assert len(entries) == 1
        assert entries[0].detail == detail


def test_sqlite_reopen_duplicate_id_rejected(tmp_path) -> None:
    """Duplicate IDs must be rejected even after a close/reopen cycle."""
    db = tmp_path / "prov.sqlite"
    run = new_run_id()
    fixed_id = "prov-fixed-reopen"

    with ProvenanceLog(db) as log1:
        log1.record(ProvenanceKind.NOTE, run_id=run, entry_id=fixed_id)

    with ProvenanceLog(db) as log2:
        with pytest.raises(ValueError):
            log2.record(ProvenanceKind.NOTE, run_id=run, entry_id=fixed_id)


def test_sqlite_multi_run_filtering(tmp_path) -> None:
    """Entries from different runs must be correctly filtered."""
    db = tmp_path / "prov.sqlite"
    run_a = new_run_id()
    run_b = new_run_id()

    with ProvenanceLog(db) as log1:
        log1.record(ProvenanceKind.ARTIFACT_INGEST, run_id=run_a)
        log1.record(ProvenanceKind.ARTIFACT_INGEST, run_id=run_b)
        log1.record(ProvenanceKind.MATCH_STAGE, run_id=run_b)

    with ProvenanceLog(db) as log2:
        assert len(log2.list_for_run(run_a)) == 1
        assert len(log2.list_for_run(run_b)) == 2
        assert len(log2.list_all()) == 3
