from __future__ import annotations
from dataclasses import dataclass,field
from datetime import datetime,timezone
from pathlib import Path
from .requirements import RequirementGraph
from .audit_pipeline import audit_tender,audit_summary
from .tenant import User,assert_tenant_access
from .document_parser import extract_text

@dataclass
class TenderProject:
    project_id: str
    name: str
    requirement_graph: RequirementGraph
    response_documents: list[str]=field(default_factory=list)
    tenant_id: str|None=None
    created_at: datetime=field(default_factory=lambda: datetime.now(timezone.utc))

def _response_text(document: str) -> str:
    path=Path(document)
    if path.is_file():
        return extract_text(path)
    return document

def audit_project(project: TenderProject,user:User|None=None)->dict:
    if project.tenant_id and user is not None: assert_tenant_access(user,project.tenant_id)
    records=[]
    for document in project.response_documents:
        records.extend(audit_tender(project.requirement_graph,_response_text(document)))
    summary=audit_summary(records)
    return {"project_id":project.project_id,"name":project.name,"summary":summary,"records":records}
