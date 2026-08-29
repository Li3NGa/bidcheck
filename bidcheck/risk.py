from __future__ import annotations
from dataclasses import dataclass
from .requirements import Requirement, RequirementType
from .response_map import ResponseMatch

@dataclass(frozen=True)
class RiskItem:
    requirement_id: str
    level: str
    score: float
    reason: str

def score_risk(requirement: Requirement, match: ResponseMatch) -> RiskItem:
    base = 0.0
    if requirement.mandatory: base += 0.55
    if requirement.type in {RequirementType.REJECTION, RequirementType.QUALIFICATION, RequirementType.DEADLINE}: base += 0.25
    if match.status == "unmatched": base += 0.20
    elif match.status == "review": base += 0.10
    elif match.status == "matched": base -= 0.20
    score=max(0.0,min(1.0,base))
    level="critical" if score>=0.8 else "high" if score>=0.6 else "medium" if score>=0.35 else "low"
    return RiskItem(requirement.id,level,score,f"{requirement.type.value}:{match.status}")
