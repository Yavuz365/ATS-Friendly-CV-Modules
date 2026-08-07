"""Append-only provenance log for search, screening and artifacts (EVAL-002).

The ledger records what the research engine actually did. It does not claim
commercial ATS behaviour. Missing fields remain explicit and are never filled
with a successful state.
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


class ProvenanceStorageError(RuntimeError):
    """Raised when persisted provenance cannot be decoded safely."""


@dataclass(frozen=True)
class ProvenanceEntry:
    id: str
    kind: ProvenanceKind
    occurred_at: str
    run_id: str
    subject_id: str | None = None
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
    """Append-only provenance ledger with optional durable SQLite storage."""

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
        self._conn.execute("CREATE INDEX IF NOT EXISTS idx_prov_run ON provenance_entries(run_id, occurred_at, id)")
        self._conn.commit()

    @staticmethod
    def _row_to_entry(row: sqlite3.Row) -> ProvenanceEntry:
        try:
            parent_ids = json.loads(row["parent_ids_json"])
            detail = json.loads(row["detail_json"])
            if not isinstance(parent_ids, list) or not all(isinstance(item, str) for item in parent_ids):
                raise TypeError("parent_ids_json must decode to a list of strings")
            if not isinstance(detail, dict):
                raise TypeError("detail_json must decode to an object")
            return ProvenanceEntry(
                id=str(row["id"]),
                kind=ProvenanceKind(row["kind"]),
                occurred_at=str(row["occurred_at"]),
                run_id=str(row["run_id"]),
                subject_id=row["subject_id"],
                parent_ids=tuple(parent_ids),
                status=row["status"],
                detail=detail,
                actor=str(row["actor"]),
            )
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            row_id = row["id"] if "id" in row.keys() else "unknown"
            raise ProvenanceStorageError(f"Invalid persisted provenance entry: {row_id}") from exc

    def append(self, entry: ProvenanceEntry) -> ProvenanceEntry:
        if any(existing.id == entry.id for existing in self._entries):
            raise ValueError(f"Provenance entry already exists: {entry.id}")

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

        self._entries.append(entry)
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
        if self._conn is None:
            return [entry for entry in self._entries if entry.run_id == run_id]
        rows = self._conn.execute(
            """
            SELECT id, kind, occurred_at, run_id, subject_id,
                   parent_ids_json, status, detail_json, actor
            FROM provenance_entries
            WHERE run_id = ?
            ORDER BY occurred_at, id
            """,
            (run_id,),
        ).fetchall()
        return [self._row_to_entry(row) for row in rows]

    def list_all(self) -> list[ProvenanceEntry]:
        if self._conn is None:
            return list(self._entries)
        rows = self._conn.execute(
            """
            SELECT id, kind, occurred_at, run_id, subject_id,
                   parent_ids_json, status, detail_json, actor
            FROM provenance_entries
            ORDER BY occurred_at, id
            """
        ).fetchall()
        return [self._row_to_entry(row) for row in rows]

    def to_jsonable(self, run_id: str | None = None) -> list[dict[str, Any]]:
        rows = self.list_for_run(run_id) if run_id else self.list_all()
        output: list[dict[str, Any]] = []
        for entry in rows:
            payload = asdict(entry)
            payload["kind"] = entry.kind.value
            payload["parent_ids"] = list(entry.parent_ids)
            output.append(payload)
        return output
