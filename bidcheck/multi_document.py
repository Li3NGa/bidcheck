from __future__ import annotations
from dataclasses import dataclass
from .requirements import RequirementGraph
from .response_map import map_responses, ResponseMatch

@dataclass(frozen=True)
class EvidenceBundle:
    requirement_id: str
    matches: tuple[ResponseMatch, ...]
    best_status: str
    best_excerpt: str

def aggregate_responses(graph: RequirementGraph, documents: list[str]) -> list[EvidenceBundle]:
    grouped: dict[str,list[ResponseMatch]]={r.id:[] for r in graph.requirements}
    for text in documents:
        for match in map_responses(graph,text): grouped[match.requirement_id].append(match)
    result=[]
    rank={"matched":3,"review":2,"unmatched":1}
    for req in graph.requirements:
        matches=grouped[req.id]
        best=max(matches,key=lambda m:(rank.get(m.status,0),m.score),default=ResponseMatch(req.id,"unmatched","",0.0))
        result.append(EvidenceBundle(req.id,tuple(matches),best.status,best.response_excerpt))
    return result
