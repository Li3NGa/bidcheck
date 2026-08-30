from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout
from dataclasses import dataclass
from time import monotonic
from .ai_provider import AIJudgement, AuditAIProvider

@dataclass(frozen=True)
class ProviderPolicy:
    timeout_seconds: float = 30.0
    max_attempts: int = 2
    cost_per_call: float = 0.0

@dataclass(frozen=True)
class ProviderUsage:
    calls: int = 0
    failures: int = 0
    estimated_cost: float = 0.0
    last_latency_seconds: float = 0.0

class ProviderRuntime:
    def __init__(self, provider: AuditAIProvider, policy: ProviderPolicy | None = None):
        self.provider = provider
        self.policy = policy or ProviderPolicy()
        self.usage = ProviderUsage()

    def judge(self, requirement: str, response: str, evidence: str) -> AIJudgement:
        if self.policy.timeout_seconds <= 0 or self.policy.max_attempts < 1 or self.policy.cost_per_call < 0:
            raise ValueError('invalid provider policy')
        last: Exception | None = None
        failures = 0
        for _ in range(self.policy.max_attempts):
            started = monotonic()
            executor = ThreadPoolExecutor(max_workers=1)
            future = executor.submit(self.provider.judge, requirement, response, evidence)
            try:
                result = future.result(timeout=self.policy.timeout_seconds)
                elapsed = monotonic() - started
                if not 0 <= result.confidence <= 1:
                    raise ValueError('invalid provider confidence')
                if result.status not in {'matched', 'missing', 'review', 'conflict'}:
                    raise ValueError('invalid provider status')
                if result.status != 'missing' and not result.evidence.strip():
                    raise ValueError('non-missing judgement requires evidence')
                self.usage = ProviderUsage(self.usage.calls + 1, self.usage.failures + failures, self.usage.estimated_cost + self.policy.cost_per_call, elapsed)
                return result
            except FutureTimeout as exc:
                last = TimeoutError('provider timeout')
                failures += 1
                future.cancel()
            except Exception as exc:
                last = exc
                failures += 1
            finally:
                executor.shutdown(wait=False, cancel_futures=True)
        self.usage = ProviderUsage(self.usage.calls, self.usage.failures + failures, self.usage.estimated_cost, self.usage.last_latency_seconds)
        raise RuntimeError('provider failed') from last
