from __future__ import annotations
from dataclasses import asdict
from .plans import Plan, FREE
from .limits import UsageLimit

def plan_entitlements(plan:Plan=FREE,usage:UsageLimit|None=None)->dict:
    usage=usage or UsageLimit(plan.daily_audits)
    return {'plan':plan.name,'daily_audits':plan.daily_audits,'audits_used':usage.audits_today,'audits_remaining':max(0,plan.daily_audits-usage.audits_today),'max_documents':plan.max_documents,'export_report':plan.export_report}

def require_export(plan:Plan)->None:
    if not plan.export_report: raise PermissionError('report export requires a paid plan')
