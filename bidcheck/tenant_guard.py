from __future__ import annotations
from .tenant import User
from .project import TenderProject

def require_project_access(project:TenderProject,user:User)->None:
    if project.tenant_id is None:
        raise PermissionError('project has no tenant owner')
    if user.tenant_id != project.tenant_id:
        raise PermissionError('tenant access denied')
