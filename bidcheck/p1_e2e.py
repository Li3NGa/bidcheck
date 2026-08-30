from __future__ import annotations
from pathlib import Path
from .document_parser import extract_text
from .requirement_extractor import extract_requirements
from .response_matcher import match_requirements

def run_audit(tender_path: str | Path, response_path: str | Path, max_bytes: int = 20_000_000) -> dict:
    tender_text = extract_text(tender_path, max_bytes)
    response_text = extract_text(response_path, max_bytes)
    graph = extract_requirements(tender_text)
    matches = match_requirements(graph, response_text)
    counts = {status: 0 for status in ('matched', 'review', 'missing', 'conflict')}
    for item in matches:
        counts[item.status] = counts.get(item.status, 0) + 1
    return {
        'tender': Path(tender_path).name,
        'response': Path(response_path).name,
        'requirements': len(graph.requirements),
        'summary': counts,
        'matches': [
            {'requirement_id': m.requirement_id, 'status': m.status,
             'evidence': m.evidence, 'confidence': m.confidence}
            for m in matches
        ],
    }
