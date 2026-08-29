from __future__ import annotations
from dataclasses import dataclass
from .requirements import Requirement

@dataclass(frozen=True)
class Verification:
    requirement_id: str
    status: str
    confidence: float
    evidence: list[str]
    reason: str

def build_verification_input(requirement: Requirement, response_excerpt: str) -> dict:
    return {
        "task": "verify_tender_response",
        "requirement": {"id": requirement.id, "type": requirement.type.value, "text": requirement.text, "page": requirement.page},
        "response": response_excerpt,
        "rules": [
            "Only use supplied evidence.",
            "Do not infer a qualification or certificate that is not evidenced.",
            "Distinguish matched, partial, unmatched and needs_review.",
            "Return confidence from 0 to 1.",
        ],
        "output_schema": {"status": "matched|partial|unmatched|needs_review", "confidence": "0..1", "evidence": ["string"], "reason": "string"},
    }
