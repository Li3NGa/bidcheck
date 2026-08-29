from __future__ import annotations
from dataclasses import asdict
from .requirements import RequirementGraph
from .response_map import map_responses
from .risk import score_risk

def build_risk_report(graph: RequirementGraph, response_text: str) -> dict:
    items=[]
    for req, match in zip(graph.requirements, map_responses(graph, response_text)):
        risk=score_risk(req, match)
        items.append({**asdict(risk), "page": req.page, "title": req.title, "requirement_type": req.type.value, "response_excerpt": match.response_excerpt})
    return {"summary":{"total":len(items),"critical":sum(x["level"]=="critical" for x in items),"high":sum(x["level"]=="high" for x in items),"review":sum(x["level"]=="medium" for x in items)},"items":items}
