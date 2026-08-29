from __future__ import annotations
from pathlib import Path
from .api import BidCheckService
from .workflow import build_project_from_document
from .response_workflow import attach_response_document

def create_from_tender(service:BidCheckService,project_id:str,name:str,tender_path:str|Path)->dict:
    project=build_project_from_document(project_id,name,tender_path)
    return service.create_project(project)

def attach_response(service:BidCheckService,project_id:str,response_path:str|Path)->dict:
    project=service.get_project(project_id)
    attach_response_document(project,response_path)
    service.repository.save(project)
    return {'project_id':project_id,'response_documents':len(project.response_documents)}

def audit(service:BidCheckService,project_id:str)->dict:
    return service.audit(project_id)
