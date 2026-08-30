from bidcheck.p1_e2e import run_audit

def test_run_audit(tmp_path):
    tender=tmp_path/'tender.txt'; response=tmp_path/'response.txt'
    tender.write_text('资格条件：具有建筑资质\n须附：营业执照\n截止时间：2026-09-01',encoding='utf-8')
    response.write_text('具有建筑资质\n营业执照已附',encoding='utf-8')
    result=run_audit(tender,response)
    assert result['requirements']==3
    assert result['summary']['matched']==2
    assert result['summary']['missing']==1
