from __future__ import annotations
from dataclasses import dataclass
import re
from .requirements import Requirement, RequirementGraph
@dataclass(frozen=True)
class ResponseMatch:
    requirement_id:str; status:str; response_excerpt:str; score:float

def map_responses(graph:RequirementGraph,response_text:str)->list[ResponseMatch]:
    out=[]
    normalized=response_text.lower()
    for req in graph.requirements:
        terms=[x for x in re.findall(r"[\u4e00-\u9fff]{2,}|[A-Za-z0-9]{3,}",req.text.lower()) if x not in {"投标","要求","提供","项目"}]
        hits=sum(1 for t in terms if t in normalized)
        score=min(1.0,hits/max(1,min(5,len(terms))))
        status="matched" if score>=0.6 else "review" if score>0 else "unmatched"
        out.append(ResponseMatch(req.id,status,"",score))
    return out
