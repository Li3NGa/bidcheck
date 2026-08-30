from __future__ import annotations
from pathlib import Path
from .document_parser import extract_text
from .requirement_extractor import extract_requirements
from .response_matcher import match_requirements

_STATUSES=('matched','review','missing','conflict')

def run_audit(tender_path: str | Path, response_path: str | Path, max_bytes: int = 20_000_000) -> dict:
    tender_text = extract_text(tender_path, max_bytes)
    response_text = extract_text(response_path, max_bytes)
    graph = extract_requirements(tender_text)
    matches = match_requirements(graph, response_text)
    counts = {status: 0 for status in _STATUSES}
    findings=[]
    for item in matches:
        status=item.status if item.status in _STATUSES else 'review'
        counts[status]+=1
        findings.append({'requirement_id':item.requirement_id,'status':status,'evidence':item.evidence,'confidence':max(0.0,min(1.0,float(item.confidence)))})
    return {'tender':Path(tender_path).name,'response':Path(response_path).name,'requirements':len(graph.requirements),'summary':counts,'matches':findings}
