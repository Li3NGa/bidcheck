from __future__ import annotations
from typing import Any
from .api import BidCheckService
from .project import TenderProject
from .serialization import graph_from_dict
from .auth_middleware import authenticate_bearer
from .session import SessionStore

class APIError(Exception):
    def __init__(self,status:int,code:str,message:str): self.status=status; self.code=code; self.message=message

def _auth(authorization:str|None,sessions:SessionStore|None):
    if sessions is None: return None
    if not authorization: raise APIError(401,'authentication_required','authentication required')
    return authenticate_bearer(authorization,sessions)

def create_project(service:BidCheckService,payload:dict[str,Any],authorization:str|None=None,sessions:SessionStore|None=None)->dict[str,Any]:
    user=_auth(authorization,sessions)
    if not isinstance(payload,dict) or not payload.get('project_id') or not payload.get('name') or not isinstance(payload.get('requirement_graph'),dict): raise APIError(400,'invalid_project','project_id, name and requirement_graph object are required')
    try: graph=graph_from_dict(payload['requirement_graph'])
    except (KeyError,TypeError,ValueError) as exc: raise APIError(400,'invalid_graph',str(exc)) from exc
    tenant_id=payload.get('tenant_id') or (user.tenant_id if user is not None else None)
    try: return service.create_project(TenderProject(str(payload['project_id']),str(payload['name']),graph,list(payload.get('response_documents',[])),tenant_id))
    except ValueError as exc: raise APIError(409,'already_exists',str(exc)) from exc
    except PermissionError as exc: raise APIError(403,'plan_limit',str(exc)) from exc

def list_projects(service:BidCheckService,authorization:str|None=None,sessions:SessionStore|None=None)->list[dict[str,Any]]:
    user=_auth(authorization,sessions)
    projects=service.list_projects()
    if user is None: return projects
    return [p for p in projects if p.get('tenant_id')==user.tenant_id]

def get_project(service:BidCheckService,project_id:str,authorization:str|None=None,sessions:SessionStore|None=None)->dict[str,Any]:
    user=_auth(authorization,sessions)
    try: project=service.get_project(project_id)
    except KeyError as exc: raise APIError(404,'not_found','project not found') from exc
    if user is not None and project.tenant_id != user.tenant_id: raise APIError(403,'forbidden','project access denied')
    return {'project_id':project.project_id,'name':project.name,'tenant_id':project.tenant_id,'response_documents':list(project.response_documents)}

def audit_project(service:BidCheckService,project_id:str,authorization:str|None=None,sessions:SessionStore|None=None)->dict[str,Any]:
    user=_auth(authorization,sessions)
    try: project=service.get_project(project_id)
    except KeyError as exc: raise APIError(404,'not_found','project not found') from exc
    if user is not None and project.tenant_id != user.tenant_id: raise APIError(403,'forbidden','project access denied')
    return service.audit(project_id)
