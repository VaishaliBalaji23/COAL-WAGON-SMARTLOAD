from pathlib import Path
import sqlite3
import json
from datetime import datetime

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "smartload.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            wagon_id TEXT NOT NULL,
            siding_id TEXT,
            wagon_type TEXT,
            gross_weight_kg REAL,
            target_weight_kg REAL,
            pll_limit_kg REAL,
            left_pct REAL,
            right_pct REAL,
            front_pct REAL,
            rear_pct REAL,
            scenario TEXT,
            risk_label TEXT,
            risk_probability REAL,
            recommended_action TEXT,
            confidence REAL,
            payload_json TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_telemetry(record: dict):
    conn = get_connection()
    conn.execute("""
        INSERT INTO telemetry (
            timestamp, wagon_id, siding_id, wagon_type,
            gross_weight_kg, target_weight_kg, pll_limit_kg,
            left_pct, right_pct, front_pct, rear_pct,
            scenario, risk_label, risk_probability,
            recommended_action, confidence, payload_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record.get("timestamp", datetime.now().isoformat()),
        record.get("wagon_id", "UNKNOWN"),
        record.get("siding_id"),
        record.get("wagon_type"),
        record.get("gross_weight_kg"),
        record.get("target_weight_kg"),
        record.get("pll_limit_kg"),
        record.get("left_pct"),
        record.get("right_pct"),
        record.get("front_pct"),
        record.get("rear_pct"),
        record.get("scenario"),
        record.get("risk_label"),
        record.get("risk_probability"),
        record.get("recommended_action"),
        record.get("confidence"),
        json.dumps(record, default=str)
    ))
    conn.commit()
    conn.close()

def recent_telemetry(limit=100):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM telemetry ORDER BY id DESC LIMIT ?", (int(limit),)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
