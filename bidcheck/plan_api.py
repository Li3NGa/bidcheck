from __future__ import annotations
from .api import BidCheckService
from .entitlements import plan_entitlements

def current_plan(service:BidCheckService)->dict:
    return plan_entitlements(service.plan,service.usage)
