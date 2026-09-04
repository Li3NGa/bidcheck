import pytest
from bidcheck.api import BidCheckService
from bidcheck.entitlements import plan_entitlements,require_export
from bidcheck.plans import FREE,PRO
from bidcheck.store import MemoryProjectRepository

def test_free_entitlements_report_remaining_usage():
    service=BidCheckService(MemoryProjectRepository())
    service.usage.consume_audit()
    result=plan_entitlements(service.plan,service.usage)
    assert result['plan']=='free'
    assert result['audits_used']==1
    assert result['audits_remaining']==2

def test_free_plan_blocks_export():
    with pytest.raises(PermissionError): require_export(FREE)
    require_export(PRO)
