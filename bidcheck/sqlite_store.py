from __future__ import annotations
import sqlite3
from pathlib import Path
from .project import TenderProject

class SQLiteProjectRepository:
    def __init__(self, path: str|Path='bidcheck.db'):
        self.path=str(path)
        with sqlite3.connect(self.path) as db:
            db.execute('CREATE TABLE IF NOT EXISTS projects (project_id TEXT PRIMARY KEY, name TEXT NOT NULL, response_documents TEXT NOT NULL, created_at TEXT NOT NULL)')
            db.commit()
    def save(self, project: TenderProject)->None:
        import json
        with sqlite3.connect(self.path) as db:
            db.execute('INSERT OR REPLACE INTO projects(project_id,name,response_documents,created_at) VALUES(?,?,?,?)',(project.project_id,project.name,json.dumps(project.response_documents,ensure_ascii=False),project.created_at.isoformat()))
            db.commit()
    def get(self, project_id:str)->TenderProject|None:
        import json
        from datetime import datetime
        with sqlite3.connect(self.path) as db:
            row=db.execute('SELECT project_id,name,response_documents,created_at FROM projects WHERE project_id=?',(project_id,)).fetchone()
        if row is None:return None
        return TenderProject(row[0],row[1],None,json.loads(row[2]),datetime.fromisoformat(row[3]))
