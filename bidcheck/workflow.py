from __future__ import annotations
from pathlib import Path
from .document_parser import extract_text
from .project import TenderProject
from .requirements import RequirementGraph,Requirement,RequirementType

def build_project_from_document(project_id:str,name:str,path:str|Path)->TenderProject:
    text=extract_text(path)
    graph=RequirementGraph()
    for i,line in enumerate((x.strip() for x in text.splitlines()),1):
        if not line: continue
        if any(k in line for k in ('必须','应当','资格','资质','要求')):
            graph.add(Requirement(f'r{i}',RequirementType.COMPLIANCE,line,line,i,True))
    return TenderProject(project_id,name,graph,[str(path)])
