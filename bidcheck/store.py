from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol
from .project import TenderProject

class ProjectRepository(Protocol):
    def save(self, project: TenderProject) -> None: ...
    def get(self, project_id: str) -> TenderProject | None: ...
    def list(self) -> list[TenderProject]: ...

@dataclass
class MemoryProjectRepository:
    projects: dict[str, TenderProject]
    def __init__(self): self.projects={}
    def save(self, project: TenderProject) -> None: self.projects[project.project_id]=project
    def get(self, project_id: str) -> TenderProject | None: return self.projects.get(project_id)
    def list(self) -> list[TenderProject]: return list(self.projects.values())
