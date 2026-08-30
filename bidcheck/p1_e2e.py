from __future__ import annotations
from pathlib import Path
from .file_ingest import ingest_text
from .requirement_extractor import extract_requirements
from .response_matcher import match_requirements

def run_audit(tender_path:str|Path,response_path:str|Path,max_bytes:int=5_000_000)->dict:
    tender=ingest_text(tender_path,max_bytes); response=ingest_text(response_path,max_bytes)
    graph=extract_requirements(tender.text)
    matches=match_requirements(graph,response.text)
    counts={'matched':0,'review':0,'missing':0}
    for item in matches: counts[item.status]+=1
    return {'tender':tender.name,'response':response.name,'requirements':len(graph.requirements),'summary':counts,'matches':[{'requirement_id':m.requirement_id,'status':m.status,'evidence':m.evidence,'confidence':m.confidence} for m in matches]}
