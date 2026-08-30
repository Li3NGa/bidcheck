from pathlib import Path
from bidcheck.p1_e2e import run_audit

def test_run_audit_from_real_txt_files(tmp_path: Path):
    tender=tmp_path/'tender.txt'; response=tmp_path/'response.txt'
    tender.write_text('投标人资格要求：具有软件开发经验\n报价要求：总价不超过100万元',encoding='utf-8')
    response.write_text('我司具有软件开发经验\n项目总价80万元',encoding='utf-8')
    result=run_audit(tender,response)
    assert result['requirements']>=1
    assert sum(result['summary'].values())==result['requirements']
    assert all(0<=item['confidence']<=1 for item in result['matches'])
