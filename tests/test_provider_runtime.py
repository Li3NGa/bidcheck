import pytest
from bidcheck.ai_provider import AIJudgement
from bidcheck.provider_runtime import ProviderPolicy, ProviderRuntime

class Provider:
    def judge(self, requirement, response, evidence):
        return AIJudgement('review', 0.7, evidence, 'review')

def test_usage_and_cost():
    runtime = ProviderRuntime(Provider(), ProviderPolicy(cost_per_call=0.02))
    result = runtime.judge('要求', '响应', '原文证据')
    assert result.evidence == '原文证据'
    assert runtime.usage.calls == 1
    assert runtime.usage.estimated_cost == 0.02

def test_invalid_status_is_rejected():
    class BadProvider(Provider):
        def judge(self, requirement, response, evidence):
            return AIJudgement('invented', 0.9, evidence, 'bad')
    with pytest.raises(RuntimeError):
        ProviderRuntime(BadProvider(), ProviderPolicy(max_attempts=1)).judge('要求', '响应', '证据')
