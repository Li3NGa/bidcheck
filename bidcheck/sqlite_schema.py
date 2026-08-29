from __future__ import annotations
import sqlite3

def init_schema(db:sqlite3.Connection)->None:
    db.executescript('''
    CREATE TABLE IF NOT EXISTS projects(project_id TEXT PRIMARY KEY,payload TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS audit_events(id INTEGER PRIMARY KEY AUTOINCREMENT,project_id TEXT NOT NULL,event_type TEXT NOT NULL,payload TEXT NOT NULL,created_at TEXT NOT NULL);
    CREATE INDEX IF NOT EXISTS idx_audit_events_project ON audit_events(project_id,created_at);
    ''')
