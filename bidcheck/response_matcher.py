from __future__ import annotations
from dataclasses import dataclass
import re
from .requirements import RequirementGraph

@dataclass(frozen=True)
class Match:
    requirement_id:str
    status:str
    evidence:str
    confidence:float

def match_requirements(graph:RequirementGraph,response_text:str)->list[Match]:
    if not isinstance(response_text,str): raise ValueError('response text is required')
    text=response_text.strip(); results=[]
    for req in graph.requirements:
        source=f'{req.title} {req.text}'.strip()
        terms=[t for t in re.findall(r'[\u4e00-\u9fffA-Za-z0-9]{2,}',source)]
        hits=[t for t in terms if t in text]
        if not hits:
            results.append(Match(req.id,'missing','',0.0)); continue
        evidence=next((line.strip() for line in text.splitlines() if any(t in line for t in hits)),hits[0])
        ratio=min(1.0,len(set(hits))/max(1,len(set(terms))))
        results.append(Match(req.id,'matched' if ratio>=0.5 else 'review',evidence,ratio))
    return results
