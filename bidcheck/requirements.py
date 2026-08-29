from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
class RequirementType(str, Enum):
    QUALIFICATION="qualification"; REJECTION="rejection"; SCORING="scoring"; TECHNICAL="technical"; COMMERCIAL="commercial"; PERSONNEL="personnel"; EXPERIENCE="experience"; ATTACHMENT="attachment"; FORMAT="format"; DEADLINE="deadline"
@dataclass(frozen=True)
class Requirement:
    id:str; type:RequirementType; title:str; text:str; page:int|None=None; mandatory:bool=False; evidence:dict[str,Any]=field(default_factory=dict)
@dataclass
class RequirementGraph:
    requirements:list[Requirement]=field(default_factory=list)
    def add(self,r:Requirement)->None:self.requirements.append(r)
    def by_type(self,k:RequirementType)->list[Requirement]:return [r for r in self.requirements if r.type is k]
