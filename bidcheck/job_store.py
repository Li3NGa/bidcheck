from __future__ import annotations
import json, sqlite3, uuid
from datetime import datetime, timezone
from pathlib import Path

class SQLiteJobStore:
    def __init__(self, path: str | Path = 'bidcheck.db'):
        self.path = str(path)
        with sqlite3.connect(self.path) as db:
            db.execute('CREATE TABLE IF NOT EXISTS jobs (job_id TEXT PRIMARY KEY, kind TEXT NOT NULL, status TEXT NOT NULL, payload TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL)')
            db.commit()

    def create(self, kind: str, payload: dict) -> dict:
        job_id = uuid.uuid4().hex
        now = datetime.now(timezone.utc).isoformat()
        record = {'job_id': job_id, 'kind': kind, 'status': 'queued', 'payload': payload, 'created_at': now, 'updated_at': now}
        with sqlite3.connect(self.path) as db:
            db.execute('INSERT INTO jobs VALUES(?,?,?,?,?,?)', (job_id, kind, 'queued', json.dumps(payload, ensure_ascii=False), now, now))
            db.commit()
        return record

    def get(self, job_id: str) -> dict | None:
        with sqlite3.connect(self.path) as db:
            row = db.execute('SELECT job_id,kind,status,payload,created_at,updated_at FROM jobs WHERE job_id=?', (job_id,)).fetchone()
        if not row: return None
        return {'job_id': row[0], 'kind': row[1], 'status': row[2], 'payload': json.loads(row[3]), 'created_at': row[4], 'updated_at': row[5]}

    def update(self, job_id: str, status: str, payload: dict | None = None) -> dict | None:
        current = self.get(job_id)
        if not current: return None
        now = datetime.now(timezone.utc).isoformat()
        data = current['payload'] if payload is None else payload
        with sqlite3.connect(self.path) as db:
            db.execute('UPDATE jobs SET status=?,payload=?,updated_at=? WHERE job_id=?', (status, json.dumps(data, ensure_ascii=False), now, job_id)); db.commit()
        return {**current, 'status': status, 'payload': data, 'updated_at': now}
