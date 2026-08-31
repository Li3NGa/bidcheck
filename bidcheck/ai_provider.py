from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Protocol

@dataclass(frozen=True)
class AIJudgement:
    status: str
    confidence: float
    evidence: str
    rationale: str

class AuditAIProvider(Protocol):
    def judge(self, requirement: str, response: str, evidence: str) -> AIJudgement: ...

class DeterministicProvider:
    """Safe fallback: never invents evidence and never upgrades missing evidence."""
    def judge(self, requirement: str, response: str, evidence: str) -> AIJudgement:
        if not evidence.strip():
            return AIJudgement('missing', 0.0, '', 'No source evidence supplied')
        return AIJudgement('review', 0.5, evidence, 'Semantic review required; deterministic provider does not infer unsupported facts.')

def audit_with_provider(requirements: Iterable, response: str, provider: AuditAIProvider, matches: Iterable) -> list[AIJudgement]:
    """Run semantic review only with evidence produced by the deterministic matcher."""
    judgements=[]
    for requirement, match in zip(requirements, matches):
        judgements.append(provider.judge(requirement.text, response, match.evidence))
    return judgements
