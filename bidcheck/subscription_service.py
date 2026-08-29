from __future__ import annotations
from datetime import datetime,timezone,timedelta
from .billing import Plan,Subscription
from .orders import Order,OrderStatus

def activate_subscription(order:Order,days:int=30,now:datetime|None=None)->Subscription:
    if order.status is not OrderStatus.PAID: raise ValueError('order is not paid')
    if days<=0: raise ValueError('days must be positive')
    now=now or datetime.now(timezone.utc)
    return Subscription(order.user_id,Plan(order.plan),True,now+timedelta(days=days))
