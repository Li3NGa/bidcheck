from __future__ import annotations
from .requirements import RequirementGraph
from .response_map import map_responses
from .audit import AuditRecord, make_audit_record
from .risk import score_risk

def audit_tender(graph: RequirementGraph, response_text: str) -> list[AuditRecord]:
    matches=map_responses(graph,response_text)
    records=[]
    for req,match in zip(graph.requirements,matches):
        records.append(make_audit_record(req,match))
    return records

def audit_summary(records: list[AuditRecord]) -> dict:
    return {"decision":"BLOCK" if any(r.decision=="BLOCK" for r in records) else "REVIEW" if any(r.decision=="REVIEW" for r in records) else "PASS","total":len(records),"blocked":sum(r.decision=="BLOCK" for r in records),"review":sum(r.decision=="REVIEW" for r in records)}
