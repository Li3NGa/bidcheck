from __future__ import annotations
from dataclasses import asdict
from typing import Any
from .api import BidCheckService
from .project import TenderProject
from .serialization import graph_from_dict

class APIError(Exception):
    def __init__(self,status:int,code:str,message:str): self.status=status; self.code=code; self.message=message

def create_project(service:BidCheckService,payload:dict[str,Any])->dict[str,Any]:
    if not isinstance(payload,dict) or not payload.get('project_id') or not payload.get('name') or not isinstance(payload.get('requirement_graph'),dict):
        raise APIError(400,'invalid_project','project_id, name and requirement_graph object are required')
    try: graph=graph_from_dict(payload['requirement_graph'])
    except (KeyError,TypeError,ValueError) as exc: raise APIError(400,'invalid_graph',str(exc)) from exc
    try: return service.create_project(TenderProject(str(payload['project_id']),str(payload['name']),graph,list(payload.get('response_documents',[]))))
    except ValueError as exc: raise APIError(409,'already_exists',str(exc)) from exc
    except PermissionError as exc: raise APIError(403,'plan_limit',str(exc)) from exc

def get_project(service:BidCheckService,project_id:str)->dict[str,Any]:
    try: return asdict(service.get_project(project_id))
    except KeyError: raise APIError(404,'not_found','project not found')

def audit_project(service:BidCheckService,project_id:str)->dict[str,Any]:
    try: return service.audit(project_id)
    except KeyError: raise APIError(404,'not_found','project not found')
    except PermissionError as exc: raise APIError(429,'rate_limit',str(exc)) from exc
