from __future__ import annotations
from dataclasses import dataclass
from time import monotonic
from typing import Callable
from .ai_provider import AIJudgement,AuditAIProvider

@dataclass(frozen=True)
class ProviderPolicy:
    timeout_seconds:float=30.0
    max_attempts:int=2

class ProviderRuntime:
    def __init__(self,provider:AuditAIProvider,policy:ProviderPolicy|None=None): self.provider=provider; self.policy=policy or ProviderPolicy()
    def judge(self,requirement:str,response:str,evidence:str)->AIJudgement:
        if self.policy.timeout_seconds<=0 or self.policy.max_attempts<1: raise ValueError('invalid provider policy')
        started=monotonic(); last=None
        for _ in range(self.policy.max_attempts):
            try:
                result=self.provider.judge(requirement,response,evidence)
                if monotonic()-started>self.policy.timeout_seconds: raise TimeoutError('provider timeout')
                if not 0<=result.confidence<=1: raise ValueError('invalid provider confidence')
                return result
            except Exception as exc: last=exc
        raise RuntimeError('provider failed') from last
