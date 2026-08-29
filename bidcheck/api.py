from __future__ import annotations
from dataclasses import asdict
from .project import TenderProject, audit_project
from .store import ProjectRepository
from .limits import UsageLimit
from .plans import Plan, FREE

class BidCheckService:
    def __init__(self, repository: ProjectRepository, plan: Plan = FREE):
        self.repository=repository; self.plan=plan; self.usage=UsageLimit(daily_audits=plan.daily_audits)
    def create_project(self, project: TenderProject) -> dict:
        if self.repository.get(project.project_id) is not None: raise ValueError("project already exists")
        if len(project.response_documents)>self.plan.max_documents: raise PermissionError("document limit reached")
        self.repository.save(project); return {"project_id":project.project_id,"name":project.name}
    def get_project(self, project_id: str) -> TenderProject:
        project=self.repository.get(project_id)
        if project is None: raise KeyError(project_id)
        return project
    def audit(self, project_id: str) -> dict:
        self.usage.consume_audit()
        project=self.get_project(project_id)
        result=audit_project(project); result["records"]=[asdict(record) for record in result["records"]]
        return result
