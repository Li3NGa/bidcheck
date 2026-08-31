from __future__ import annotations
import json,sqlite3
from pathlib import Path
from .project import TenderProject
from .project_serialization import project_to_dict,project_from_dict

class SQLiteProjectRepository:
    def __init__(self,path:str|Path='bidcheck.db'):
        self.path=str(path)
        with sqlite3.connect(self.path) as db:
            db.execute('CREATE TABLE IF NOT EXISTS projects (project_id TEXT PRIMARY KEY, payload TEXT NOT NULL)'); db.commit()
    def save(self,project:TenderProject)->None:
        payload=json.dumps(project_to_dict(project),ensure_ascii=False)
        with sqlite3.connect(self.path) as db:
            db.execute('INSERT OR REPLACE INTO projects(project_id,payload) VALUES(?,?)',(project.project_id,payload)); db.commit()
    def get(self,project_id:str)->TenderProject|None:
        with sqlite3.connect(self.path) as db: row=db.execute('SELECT payload FROM projects WHERE project_id=?',(project_id,)).fetchone()
        return project_from_dict(json.loads(row[0])) if row else None
    def list(self)->list[TenderProject]:
        with sqlite3.connect(self.path) as db: rows=db.execute('SELECT payload FROM projects ORDER BY project_id').fetchall()
        return [project_from_dict(json.loads(row[0])) for row in rows]
