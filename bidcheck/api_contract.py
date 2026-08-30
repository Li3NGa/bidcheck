from __future__ import annotations
from dataclasses import dataclass
from typing import Any,Callable

@dataclass(frozen=True)
class EndpointResult:
    status:int; body:dict[str,Any]

def project_create(payload:dict[str,Any])->EndpointResult:
    if not isinstance(payload,dict) or not payload.get('project_id') or not payload.get('name'): return EndpointResult(400,{'error':'invalid_project'})
    return EndpointResult(201,{'project_id':str(payload['project_id']),'name':str(payload['name'])})

def audit_execute(project_id:str,runner:Callable[[str],dict[str,Any]])->EndpointResult:
    if not project_id: return EndpointResult(400,{'error':'invalid_project_id'})
    try:return EndpointResult(200,{'status':'completed','result':runner(project_id)})
    except Exception:return EndpointResult(500,{'error':'audit_failed'})
