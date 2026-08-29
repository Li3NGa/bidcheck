from __future__ import annotations
import json
from .audit_pipeline import audit_tender, audit_summary
from .requirements import RequirementGraph

def export_report(graph: RequirementGraph, response_text: str) -> str:
    records=audit_tender(graph,response_text)
    payload={"summary":audit_summary(records),"records":[{"requirement_id":r.requirement_id,"page":r.requirement_page,"match_status":r.match_status,"verification_status":r.verification_status,"evidence":r.evidence,"decision":r.decision} for r in records]}
    return json.dumps(payload,ensure_ascii=False,indent=2)
