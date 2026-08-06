"""Append-only provenance log for search, screening and artifacts (EVAL-002).

Purpose
-------
Record *what this engine actually did* during an evaluation or screening run:
which artifact was ingested, which requirements were considered, which matcher
stages fired, and which decision/gate outcomes were produced.

This is not a commercial ATS audit log and does not claim vendor behaviour.
Entries are immutable once appended. Missing fields stay explicit (None),
never silently filled with success.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any
from uuid import uuid4


class ProvenanceKind(str, Enum):
    ARTIFACT_INGEST = "ARTIFACT_INGEST"
    REQUIREMENT_EXTRACT = "REQUIREMENT_EXTRACT"
    MATCH_STAGE = "MATCH_STAGE"
    SCREENING_DECISION = "SCREENING_DECISION"
    EVALUATION_RUN = "EVALUATION_RUN"
    NOTE = "NOTE"


@dataclass(frozen=True)
class ProvenanceEntry:
    id: str
    kind: ProvenanceKind
    occurred_at: str
    run_id: str
    subject_id: str | None = None  # artifact / requirement / candidate id
    parent_ids: tuple[str, ...] = ()
    status: str | None = None
    detail: dict[str, Any] = field(default_factory=dict)
    actor: str = "ats-engine"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_run_id() -> str:
    return f"run-{uuid4().hex[:12]}"


def new_entry_id() -> str:
    return f"prov-{uuid4().hex[:16]}"


class ProvenanceLog:
    """In-memory append-only provenance ledger.

    Optional SQLite path enables durable evaluation runs without coupling to
    the full contract store.
    """

    def __init__(self, path: str | Path | None = None) -> None:
        self._entries: list[ProvenanceEntry] = []
        self._path = str(path) if path is not None else None
        self._conn: sqlite3.Connection | None = None
        if self._path and self._path != ":memory:":
            Path(self._path).expanduser().resolve().parent.mkdir(parents=True, exist_ok=True)
        if self._path is not None:
            self._conn = sqlite3.connect(self._path)
            self._conn.row_factory = sqlite3.Row
            self._migrate()

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def __enter__(self) -> ProvenanceLog:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def _migrate(self) -> None:
        assert self._conn is not None
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS provenance_entries (
                id TEXT PRIMARY KEY,
                kind TEXT NOT NULL,
                occurred_at TEXT NOT NULL,
                run_id TEXT NOT NULL,
                subject_id TEXT,
                parent_ids_json TEXT NOT NULL,
                status TEXT,
                detail_json TEXT NOT NULL,
                actor TEXT NOT NULL
            )
            """
        )
        self._conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_prov_run ON provenance_entries(run_id, occurred_at)"
        )
        self._conn.commit()

    def append(self, entry: ProvenanceEntry) -> ProvenanceEntry:
        if any(e.id == entry.id for e in self._entries):
            raise ValueError(f"Provenance entry already exists: {entry.id}")
        self._entries.append(entry)
        if self._conn is not None:
            try:
                with self._conn:
                    self._conn.execute(
                        """
                        INSERT INTO provenance_entries(
                            id, kind, occurred_at, run_id, subject_id,
                            parent_ids_json, status, detail_json, actor
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            entry.id,
                            entry.kind.value,
                            entry.occurred_at,
                            entry.run_id,
                            entry.subject_id,
                            json.dumps(list(entry.parent_ids), ensure_ascii=False),
                            entry.status,
                            json.dumps(entry.detail, ensure_ascii=False, sort_keys=True),
                            entry.actor,
                        ),
                    )
            except sqlite3.IntegrityError as exc:
                raise ValueError(f"Provenance entry already exists: {entry.id}") from exc
        return entry

    def record(
        self,
        kind: ProvenanceKind,
        *,
        run_id: str,
        subject_id: str | None = None,
        parent_ids: list[str] | tuple[str, ...] | None = None,
        status: str | None = None,
        detail: dict[str, Any] | None = None,
        actor: str = "ats-engine",
        entry_id: str | None = None,
        occurred_at: str | None = None,
    ) -> ProvenanceEntry:
        entry = ProvenanceEntry(
            id=entry_id or new_entry_id(),
            kind=kind,
            occurred_at=occurred_at or _utc_now(),
            run_id=run_id,
            subject_id=subject_id,
            parent_ids=tuple(parent_ids or ()),
            status=status,
            detail=dict(detail or {}),
            actor=actor,
        )
        return self.append(entry)

    def list_for_run(self, run_id: str) -> list[ProvenanceEntry]:
        return [e for e in self._entries if e.run_id == run_id]

    def list_all(self) -> list[ProvenanceEntry]:
        return list(self._entries)

    def to_jsonable(self, run_id: str | None = None) -> list[dict[str, Any]]:
        rows = self.list_for_run(run_id) if run_id else self.list_all()
        out: list[dict[str, Any]] = []
        for e in rows:
            payload = asdict(e)
            payload["kind"] = e.kind.value
            payload["parent_ids"] = list(e.parent_ids)
            out.append(payload)
        return out
