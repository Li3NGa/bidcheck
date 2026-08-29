from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from datetime import datetime,timezone
from uuid import uuid4

class OrderStatus(str,Enum): PENDING='pending'; PAID='paid'; CANCELED='canceled'

@dataclass
class Order:
    user_id:str
    plan:str
    amount:int
    order_id:str=''
    status:OrderStatus=OrderStatus.PENDING
    provider_trade_id:str|None=None
    created_at:datetime|None=None

    def __post_init__(self):
        if not self.order_id:self.order_id=uuid4().hex
        if self.created_at is None:self.created_at=datetime.now(timezone.utc)

    def mark_paid(self,trade_id:str)->None:
        if self.status is OrderStatus.PAID and self.provider_trade_id==trade_id:return
        if self.status is not OrderStatus.PENDING:raise ValueError('order is not payable')
        self.status=OrderStatus.PAID; self.provider_trade_id=trade_id
