from bidcheck.ai_provider import AIJudgement, DeterministicProvider, audit_with_provider
from bidcheck.requirements import Requirement, RequirementGraph, RequirementType
from bidcheck.response_matcher import Match

def test_provider_receives_match_evidence():
    graph=RequirementGraph([Requirement('R1',RequirementType.QUALIFICATION,'资质','具有软件开发资质',mandatory=True)])
    matches=[Match('R1','matched','响应文件：具有软件开发资质',0.9)]
    result=audit_with_provider(graph.requirements,'响应文件：具有软件开发资质',DeterministicProvider(),matches)
    assert result[0].evidence==matches[0].evidence
    assert result[0].status=='review'

def test_provider_never_invents_missing_evidence():
    result=DeterministicProvider().judge('要求','响应','')
    assert result==AIJudgement('missing',0.0,'','No source evidence supplied')
