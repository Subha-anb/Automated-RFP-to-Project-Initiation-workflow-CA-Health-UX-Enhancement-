"""State store (SQLite) and append-only audit log (JSONL)."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone

from .config import AUDIT_LOG, DB_PATH, STATE_DIR

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS stages (
    run_id INTEGER NOT NULL,
    stage INTEGER NOT NULL,
    status TEXT NOT NULL,          -- pending | running | awaiting_approval | approved | returned
    output_json TEXT,              -- latest validated agent output
    checks_json TEXT,              -- deterministic checks on that output
    error TEXT,                    -- refusal / validation / API error shown at the checkpoint
    attempt INTEGER NOT NULL DEFAULT 0,
    messages_json TEXT,            -- append-only conversation for this stage
    due_at TEXT,                   -- checkpoint SLA
    updated_at TEXT NOT NULL,
    PRIMARY KEY (run_id, stage)
);
CREATE TABLE IF NOT EXISTS decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER NOT NULL,
    stage INTEGER NOT NULL,
    attempt INTEGER NOT NULL,
    approver TEXT NOT NULL,
    decision TEXT NOT NULL,        -- approve | return
    comment TEXT,
    at TEXT NOT NULL
);
"""


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def connect() -> sqlite3.Connection:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def audit(event: str, **fields) -> None:
    """Append one event to the audit trail (rule INT-02). Never rewritten."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    record = {"at": now(), "event": event, **fields}
    with AUDIT_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def new_run(conn: sqlite3.Connection, stage_numbers) -> int:
    cur = conn.execute("INSERT INTO runs (created_at) VALUES (?)", (now(),))
    run_id = cur.lastrowid
    for n in stage_numbers:
        conn.execute(
            "INSERT INTO stages (run_id, stage, status, updated_at) VALUES (?, ?, 'pending', ?)",
            (run_id, n, now()),
        )
    conn.commit()
    audit("run_created", run_id=run_id)
    return run_id


def latest_run(conn: sqlite3.Connection) -> int | None:
    row = conn.execute("SELECT MAX(id) AS id FROM runs").fetchone()
    return row["id"] if row and row["id"] is not None else None


def get_stage(conn: sqlite3.Connection, run_id: int, stage: int) -> sqlite3.Row:
    return conn.execute("SELECT * FROM stages WHERE run_id = ? AND stage = ?", (run_id, stage)).fetchone()


def all_stages(conn: sqlite3.Connection, run_id: int) -> list[sqlite3.Row]:
    return conn.execute("SELECT * FROM stages WHERE run_id = ? ORDER BY stage", (run_id,)).fetchall()


def update_stage(conn: sqlite3.Connection, run_id: int, stage: int, **fields) -> None:
    fields["updated_at"] = now()
    cols = ", ".join(f"{k} = ?" for k in fields)
    conn.execute(f"UPDATE stages SET {cols} WHERE run_id = ? AND stage = ?", (*fields.values(), run_id, stage))
    conn.commit()


def record_decision(conn, run_id, stage, attempt, approver, decision, comment) -> None:
    conn.execute(
        "INSERT INTO decisions (run_id, stage, attempt, approver, decision, comment, at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (run_id, stage, attempt, approver, decision, comment, now()),
    )
    conn.commit()
    audit("human_decision", run_id=run_id, stage=stage, attempt=attempt, approver=approver,
          decision=decision, comment=comment)


def approvals_for_attempt(conn, run_id, stage, attempt) -> set[str]:
    rows = conn.execute(
        "SELECT approver FROM decisions WHERE run_id = ? AND stage = ? AND attempt = ? AND decision = 'approve'",
        (run_id, stage, attempt),
    ).fetchall()
    return {r["approver"] for r in rows}
