from __future__ import annotations
from dataclasses import asdict
from typing import Any
from .api import BidCheckService
from .project import TenderProject

class APIError(Exception):
    def __init__(self,status:int,code:str,message:str): self.status=status; self.code=code; self.message=message

def create_project(service:BidCheckService,payload:dict[str,Any])->dict[str,Any]:
    if not isinstance(payload,dict) or not payload.get('project_id') or not payload.get('name') or not payload.get('requirement_graph'):
        raise APIError(400,'invalid_project','project_id, name and requirement_graph are required')
    project=payload['requirement_graph']
    if not hasattr(project,'requirements'): raise APIError(400,'invalid_graph','requirement_graph must be a RequirementGraph')
    return service.create_project(TenderProject(str(payload['project_id']),str(payload['name']),project,list(payload.get('response_documents',[]))))

def get_project(service:BidCheckService,project_id:str)->dict[str,Any]:
    try: return asdict(service.get_project(project_id))
    except KeyError: raise APIError(404,'not_found','project not found')

def audit_project(service:BidCheckService,project_id:str)->dict[str,Any]:
    try: return service.audit(project_id)
    except KeyError: raise APIError(404,'not_found','project not found')
