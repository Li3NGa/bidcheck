from __future__ import annotations
from typing import Any
from .commerce import CommerceService, PLAN_PRICES_CENTS, PLANS
from .payment import PaymentNotConfigured

def pricing()->list[dict[str,Any]]:
    return [{'plan':name,'price_cents':PLAN_PRICES_CENTS[name],'daily_audits':plan.daily_audits,'max_documents':plan.max_documents,'export_report':plan.export_report} for name,plan in PLANS.items()]

def create_order(commerce:CommerceService,payload:dict[str,Any])->dict[str,Any]:
    if not isinstance(payload,dict) or not payload.get('user_id') or not payload.get('plan'): raise ValueError('user_id and plan are required')
    order=commerce.create_order(str(payload['user_id']),str(payload['plan']))
    return {'order_id':order.order_id,'user_id':order.user_id,'plan':order.plan,'amount_cents':order.amount,'status':order.status.value}

def checkout(commerce:CommerceService,order_id:str,notify_url:str)->dict[str,Any]:
    try:
        session=commerce.checkout(order_id,notify_url)
    except PaymentNotConfigured as exc:
        raise RuntimeError('payment provider is not configured') from exc
    return {'order_id':session.order_id,'provider':session.provider,'checkout_url':session.checkout_url}

def confirm(commerce:CommerceService,order_id:str,payload:bytes,signature:str)->dict[str,Any]:
    return commerce.confirm(order_id,payload,signature)

def entitlement(commerce:CommerceService,user_id:str)->dict[str,Any]:
    if not user_id.strip(): raise ValueError('user_id is required')
    return commerce.entitlement(user_id)
