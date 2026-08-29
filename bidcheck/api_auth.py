from __future__ import annotations
from .auth_middleware import authenticate_bearer
from .session import SessionStore
from .project import TenderProject,audit_project
from .tenant_guard import require_project_access

def audit_authorized(authorization:str,project:TenderProject,sessions:SessionStore)->dict:
    user=authenticate_bearer(authorization,sessions)
    require_project_access(project,user)
    return audit_project(project,user)
