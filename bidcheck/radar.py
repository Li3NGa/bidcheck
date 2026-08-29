from __future__ import annotations
from .requirements import RequirementGraph
from .response_map import map_responses
from .risk import score_risk

def build_radar(graph: RequirementGraph, response_text: str) -> dict:
    rows=[]
    for req, match in zip(graph.requirements, map_responses(graph, response_text)):
        risk=score_risk(req, match)
        rows.append({"requirement_id":req.id,"page":req.page,"type":req.type.value,"mandatory":req.mandatory,"status":match.status,"risk":risk.level,"score":risk.score})
    rows.sort(key=lambda x:x["score"], reverse=True)
    return {"decision":"BLOCK" if any(x["risk"]=="critical" for x in rows) else "REVIEW" if any(x["risk"]=="high" for x in rows) else "PASS","items":rows}
