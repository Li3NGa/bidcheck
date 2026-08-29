from bidcheck.requirements import Requirement,RequirementType
from bidcheck.response_map import ResponseMatch
from bidcheck.risk import score_risk

def test_unmatched_mandatory_rejection_is_critical():
    req=Requirement("R1",RequirementType.REJECTION,"否决投标","未签字盖章",12,True,{})
    item=score_risk(req,ResponseMatch("R1","unmatched","",0))
    assert item.level=="critical"
    assert item.score>=0.8
