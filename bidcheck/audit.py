from __future__ import annotations
from dataclasses import dataclass
from .requirements import Requirement
from .response_map import ResponseMatch
from .semantic_verify import Verification

@dataclass(frozen=True)
class AuditRecord:
    requirement_id: str
    requirement_page: int | None
    match_status: str
    verification_status: str | None
    evidence: list[str]
    decision: str

def make_audit_record(requirement: Requirement, match: ResponseMatch, verification: Verification | None = None) -> AuditRecord:
    status=verification.status if verification else match.status
    decision="BLOCK" if requirement.mandatory and status in {"unmatched","partial"} else "REVIEW" if status == "needs_review" else "PASS"
    evidence=list(verification.evidence) if verification else ([match.response_excerpt] if match.response_excerpt else [])
    return AuditRecord(requirement.id, requirement.page, match.status, verification.status if verification else None, evidence, decision)
