from __future__ import annotations
from dataclasses import asdict
from .project import TenderProject
from .serialization import graph_to_dict,graph_from_dict

def project_to_dict(project:TenderProject)->dict:
    return {"project_id":project.project_id,"name":project.name,"requirement_graph":graph_to_dict(project.requirement_graph) if project.requirement_graph else None,"response_documents":list(project.response_documents),"created_at":project.created_at.isoformat()}

def project_from_dict(data:dict)->TenderProject:
    from datetime import datetime
    graph=graph_from_dict(data["requirement_graph"]) if data.get("requirement_graph") else None
    return TenderProject(str(data["project_id"]),str(data["name"]),graph,list(data.get("response_documents",[])),datetime.fromisoformat(data["created_at"]))
