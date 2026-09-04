from __future__ import annotations
from dataclasses import dataclass
from .plans import Plan, FREE, PRO, TEAM
from .limits import UsageLimit

PLANS: dict[str, Plan] = {p.name: p for p in (FREE, PRO, TEAM)}

@dataclass
class Entitlement:
    user_id: str
    plan: str = FREE.name
    order_id: str | None = None
    active: bool = True

    def activate(self, plan: str, order_id: str | None = None) -> None:
        if plan not in PLANS: raise ValueError('unknown plan')
        self.plan = plan; self.order_id = order_id; self.active = True

def activate_paid(entitlement: Entitlement, plan: str, order_id: str, paid: bool) -> Entitlement:
    if not paid: raise PermissionError('order is not paid')
    entitlement.activate(plan, order_id); return entitlement

def plan_for(entitlement: Entitlement) -> Plan:
    return PLANS.get(entitlement.plan, FREE)

def plan_entitlements(plan: Plan = FREE, usage: UsageLimit | None = None) -> dict:
    usage = usage or UsageLimit(plan.daily_audits)
    return {'plan':plan.name,'daily_audits':plan.daily_audits,'audits_used':usage.audits_today,'audits_remaining':max(0,plan.daily_audits-usage.audits_today),'max_documents':plan.max_documents,'export_report':plan.export_report}

def require_export(plan: Plan) -> None:
    if not plan.export_report: raise PermissionError('report export requires a paid plan')
