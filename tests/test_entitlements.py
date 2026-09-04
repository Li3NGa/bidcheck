import pytest
from bidcheck.entitlements import Entitlement,activate_paid,plan_for

def test_paid_activation_changes_plan():
    item=activate_paid(Entitlement('u1'),'pro','o1',True)
    assert item.active and item.order_id=='o1' and plan_for(item).name=='pro'

def test_unpaid_order_cannot_activate():
    with pytest.raises(PermissionError): activate_paid(Entitlement('u1'),'pro','o1',False)
