from __future__ import annotations
from dataclasses import dataclass,field
from datetime import datetime,timezone
from .requirements import RequirementGraph
from .audit_pipeline import audit_tender,audit_summary

@dataclass
class TenderProject:
    project_id: str
    name: str
    requirement_graph: RequirementGraph
    response_documents: list[str]=field(default_factory=list)
    created_at: datetime=field(default_factory=lambda: datetime.now(timezone.utc))

def audit_project(project: TenderProject)->dict:
    records=[]
    for document in project.response_documents:
        records.extend(audit_tender(project.requirement_graph,document))
    summary=audit_summary(records)
    return {"project_id":project.project_id,"name":project.name,"summary":summary,"records":records}
