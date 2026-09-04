from pathlib import Path
from bidcheck.ai_provider import AIJudgement
from bidcheck.semantic_audit import semantic_audit

class Provider:
    def judge(self, requirement, response, evidence):
        return AIJudgement('matched',0.95,'hallucinated evidence','bad')

def test_semantic_audit_retains_source_evidence(tmp_path: Path):
    tender=tmp_path/'tender.txt'; response=tmp_path/'response.txt'
    tender.write_text('资格要求：具有软件开发经验',encoding='utf-8')
    response.write_text('我司具有软件开发经验',encoding='utf-8')
    result=semantic_audit(tender,response,Provider())
    finding=result['findings'][0]
    assert finding['evidence']=='我司具有软件开发经验'
    assert finding['status']=='review'
    assert finding['confidence']<=0.5
