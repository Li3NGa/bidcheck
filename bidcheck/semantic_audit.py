from __future__ import annotations
from pathlib import Path
from .ai_provider import AIJudgement, AuditAIProvider
from .document_parser import extract_text
from .requirement_extractor import extract_requirements
from .response_matcher import match_requirements
from .report import risk_for_status

def semantic_audit(tender_path: str | Path, response_path: str | Path, provider: AuditAIProvider, max_bytes: int = 20_000_000) -> dict:
    tender_text = extract_text(tender_path, max_bytes)
    response_text = extract_text(response_path, max_bytes)
    graph = extract_requirements(tender_text)
    matches = match_requirements(graph, response_text)
    judgements: list[AIJudgement] = []
    for req, match in zip(graph.requirements, matches):
        if match.status == 'missing':
            judgements.append(AIJudgement('missing', 0.0, '', 'No deterministic evidence found'))
        else:
            judgement = provider.judge(req.text, response_text, match.evidence)
            if judgement.evidence.strip() != match.evidence.strip():
                judgement = AIJudgement('review', min(judgement.confidence, 0.5), match.evidence, 'Provider evidence differs; retained deterministic evidence')
            judgements.append(judgement)
    findings=[]
    for req, match, judgement in zip(graph.requirements, matches, judgements):
        status=judgement.status if judgement.status in {'matched','review','missing','conflict'} else 'review'
        confidence=min(1.0,max(0.0,float(judgement.confidence)))
        findings.append({'requirement_id':req.id,'status':status,'evidence':match.evidence,'confidence':confidence,'risk':risk_for_status(status,confidence),'rationale':judgement.rationale})
    return {'requirements':len(graph.requirements),'findings':findings}
