from __future__ import annotations
from dataclasses import dataclass
from typing import Any,Callable

@dataclass(frozen=True)
class AuditTask:
    task_id:str; project_id:str; status:str='queued'; error:str|None=None

@dataclass(frozen=True)
class APIResult:
    status:int; data:dict[str,Any]

def enqueue_audit(project_id:str,runner:Callable[[str],dict[str,Any]])->APIResult:
    if not project_id.strip(): return APIResult(400,{'error':'invalid_project_id'})
    try: result=runner(project_id); return APIResult(200,{'status':'completed','result':result})
    except Exception: return APIResult(500,{'error':'audit_failed'})
