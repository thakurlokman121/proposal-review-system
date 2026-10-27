from __future__ import annotations

import json
import math
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


DEFAULT_CRITERIA = [
    (1, "Technical Capability", "Architecture, integrations, scalability, and technical fit", 30, 10, 1),
    (2, "Implementation Plan", "Timeline, milestones, staffing, dependencies, and risk plan", 20, 10, 1),
    (3, "Commercial Value", "Pricing clarity, total cost, and commercial assumptions", 20, 10, 1),
    (4, "Security & Compliance", "Security controls, certifications, privacy, and auditability", 20, 10, 1),
    (5, "Support & Experience", "Support model, relevant projects, and references", 10, 10, 1),
]


def database_path() -> Path:
    return Path(os.getenv("RFP_DATABASE_PATH", "rfp_evaluation.db"))


def connect() -> sqlite3.Connection:
    connection = sqlite3.connect(database_path())
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database() -> None:
    with connect() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS evaluation_criteria (
                criterion_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                description TEXT NOT NULL,
                weight REAL NOT NULL CHECK(weight >= 0 AND weight <= 100),
                max_score REAL NOT NULL CHECK(max_score > 0),
                is_active INTEGER NOT NULL DEFAULT 1 CHECK(is_active IN (0, 1))
            );
            CREATE TABLE IF NOT EXISTS rfp_runs (
                rfp_run_id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                status TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS supplier_results (
                rfp_run_id TEXT NOT NULL REFERENCES rfp_runs(rfp_run_id),
                supplier_name TEXT NOT NULL,
                submission_date TEXT NOT NULL,
                experience_rating REAL NOT NULL,
                absolute_score REAL NOT NULL,
                ppi REAL NOT NULL,
                final_rank INTEGER NOT NULL,
                result_json TEXT NOT NULL,
                PRIMARY KEY (rfp_run_id, supplier_name)
            );
            """
        )
        count = connection.execute("SELECT COUNT(*) FROM evaluation_criteria").fetchone()[0]
        if count == 0:
            connection.executemany(
                "INSERT INTO evaluation_criteria VALUES (?, ?, ?, ?, ?, ?)", DEFAULT_CRITERIA
            )


def get_active_criteria(include_inactive: bool = False) -> list[dict]:
    condition = "" if include_inactive else "WHERE is_active = 1"
    with connect() as connection:
        rows = connection.execute(
            f"SELECT criterion_id, name, description, weight, max_score, is_active FROM evaluation_criteria {condition} ORDER BY criterion_id"
        ).fetchall()
    return [dict(row) for row in rows]


def save_criteria(rows: list[dict]) -> None:
    normalized = []
    names = set()
    active_weight = 0.0
    for row in rows:
        name = str(row.get("Criterion", "")).strip()
        if not name:
            raise ValueError("Every criterion must have a name.")
        if name.casefold() in names:
            raise ValueError("Criterion names must be unique.")
        names.add(name.casefold())
        active = bool(row.get("Active", False))
        weight = float(row.get("Weight", 0))
        max_score = float(row.get("Maximum score", 0))
        if weight < 0 or weight > 100 or max_score <= 0:
            raise ValueError(f"Invalid weight or maximum score for {name}.")
        active_weight += weight if active else 0
        raw_id = row.get("ID")
        criterion_id = None if raw_id is None or (isinstance(raw_id, float) and math.isnan(raw_id)) else int(raw_id)
        normalized.append((criterion_id, name, str(row.get("Description", "")).strip(), weight, max_score, int(active)))
    if not normalized or not any(row[5] for row in normalized):
        raise ValueError("At least one criterion must be active.")
    if round(active_weight, 6) != 100:
        raise ValueError("Active criterion weights must total exactly 100%.")
    with connect() as connection:
        existing_ids = {row[0] for row in connection.execute("SELECT criterion_id FROM evaluation_criteria")}
        retained_ids = {row[0] for row in normalized if row[0] is not None}
        for row in normalized:
            if row[0] is None:
                connection.execute(
                    "INSERT INTO evaluation_criteria (name, description, weight, max_score, is_active) VALUES (?, ?, ?, ?, ?)",
                    row[1:],
                )
            else:
                connection.execute(
                    "UPDATE evaluation_criteria SET name=?, description=?, weight=?, max_score=?, is_active=? WHERE criterion_id=?",
                    (row[1], row[2], row[3], row[4], row[5], row[0]),
                )
        removed_ids = existing_ids - retained_ids
        if removed_ids:
            connection.executemany("DELETE FROM evaluation_criteria WHERE criterion_id=?", [(item,) for item in removed_ids])


def persist_run(suppliers: list[dict]) -> dict:
    run_id = str(uuid4())
    created_at = datetime.now(timezone.utc).isoformat()
    with connect() as connection:
        connection.execute("INSERT INTO rfp_runs VALUES (?, ?, ?)", (run_id, created_at, "completed"))
        connection.executemany(
            "INSERT INTO supplier_results VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            [
                (
                    run_id,
                    supplier["supplier_name"],
                    supplier["submission_date"],
                    supplier["experience_rating"],
                    supplier["absolute_score"],
                    supplier["ppi"],
                    supplier["final_rank"],
                    json.dumps(supplier, ensure_ascii=False),
                )
                for supplier in suppliers
            ],
        )
    return {"rfp_run_id": run_id, "created_at": created_at, "status": "completed", "suppliers": suppliers}


def get_latest_run() -> dict | None:
    with connect() as connection:
        run = connection.execute("SELECT * FROM rfp_runs ORDER BY created_at DESC LIMIT 1").fetchone()
        if run is None:
            return None
        suppliers = connection.execute(
            "SELECT result_json FROM supplier_results WHERE rfp_run_id=? ORDER BY final_rank", (run["rfp_run_id"],)
        ).fetchall()
    return {**dict(run), "suppliers": [json.loads(row["result_json"]) for row in suppliers]}