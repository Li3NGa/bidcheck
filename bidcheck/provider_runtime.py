from __future__ import annotations
from dataclasses import dataclass
from time import monotonic
from .ai_provider import AIJudgement,AuditAIProvider

@dataclass(frozen=True)
class ProviderPolicy:
    timeout_seconds:float=30.0
    max_attempts:int=2
    cost_per_call:float=0.0

@dataclass(frozen=True)
class ProviderUsage:
    calls:int=0
    failures:int=0
    estimated_cost:float=0.0
    last_latency_seconds:float=0.0

class ProviderRuntime:
    def __init__(self,provider:AuditAIProvider,policy:ProviderPolicy|None=None):
        self.provider=provider; self.policy=policy or ProviderPolicy(); self.usage=ProviderUsage()
    def judge(self,requirement:str,response:str,evidence:str)->AIJudgement:
        if self.policy.timeout_seconds<=0 or self.policy.max_attempts<1 or self.policy.cost_per_call<0: raise ValueError('invalid provider policy')
        started=monotonic(); last=None; failures=0
        for _ in range(self.policy.max_attempts):
            try:
                result=self.provider.judge(requirement,response,evidence)
                elapsed=monotonic()-started
                if elapsed>self.policy.timeout_seconds: raise TimeoutError('provider timeout')
                if not 0<=result.confidence<=1: raise ValueError('invalid provider confidence')
                self.usage=ProviderUsage(self.usage.calls+1,self.usage.failures+failures,self.usage.estimated_cost+self.policy.cost_per_call,elapsed)
                return result
            except Exception as exc:
                last=exc; failures+=1
        self.usage=ProviderUsage(self.usage.calls,self.usage.failures+failures,self.usage.estimated_cost,self.usage.last_latency_seconds)
        raise RuntimeError('provider failed') from last
