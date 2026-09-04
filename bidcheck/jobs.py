from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime,timezone
from typing import Callable
import json,sqlite3
from uuid import uuid4

@dataclass(frozen=True)
class AuditJob:
    job_id:str; project_id:str; status:str; result:dict|None=None; error:str|None=None; created_at:str=''

class SQLiteJobStore:
    def __init__(self,path:str='bidcheck.db'):
        self.path=path
        with sqlite3.connect(path) as db:
            db.execute('CREATE TABLE IF NOT EXISTS audit_jobs(job_id TEXT PRIMARY KEY,project_id TEXT NOT NULL,status TEXT NOT NULL,result TEXT,error TEXT,created_at TEXT NOT NULL)'); db.commit()
    def create(self,project_id:str)->AuditJob:
        job=AuditJob(uuid4().hex,project_id,'queued',created_at=datetime.now(timezone.utc).isoformat())
        with sqlite3.connect(self.path) as db: db.execute('INSERT INTO audit_jobs VALUES(?,?,?,?,?,?)',(job.job_id,job.project_id,job.status,None,None,job.created_at)); db.commit()
        return job
    def update(self,job_id:str,status:str,result:dict|None=None,error:str|None=None)->AuditJob:
        if status not in {'queued','running','completed','failed'}: raise ValueError('invalid job status')
        with sqlite3.connect(self.path) as db:
            db.execute('UPDATE audit_jobs SET status=?,result=?,error=? WHERE job_id=?',(status,json.dumps(result,ensure_ascii=False) if result is not None else None,error,job_id)); db.commit()
        return self.get(job_id)
    def get(self,job_id:str)->AuditJob:
        with sqlite3.connect(self.path) as db: row=db.execute('SELECT job_id,project_id,status,result,error,created_at FROM audit_jobs WHERE job_id=?',(job_id,)).fetchone()
        if not row: raise KeyError(job_id)
        return AuditJob(row[0],row[1],row[2],json.loads(row[3]) if row[3] else None,row[4],row[5])

class AuditJobRunner:
    def __init__(self,store:SQLiteJobStore,runner:Callable[[str],dict]): self.store=store; self.runner=runner
    def run(self,job_id:str)->AuditJob:
        job=self.store.get(job_id); self.store.update(job_id,'running')
        try: result=self.runner(job.project_id); return self.store.update(job_id,'completed',result)
        except Exception as exc: return self.store.update(job_id,'failed',error=str(exc))
