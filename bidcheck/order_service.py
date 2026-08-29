from __future__ import annotations
from .orders import Order
from .payment import PaymentProvider,PaymentRequest,PaymentSession

class OrderService:
    def __init__(self,provider:PaymentProvider): self.provider=provider
    def checkout(self,order:Order,notify_url:str)->PaymentSession:
        if order.status.value!='pending': raise ValueError('order is not payable')
        return self.provider.create_payment(PaymentRequest(order.order_id,order.amount,f'BidCheck {order.plan}',notify_url))
    def confirm(self,order:Order,payload:bytes,signature:str)->Order:
        trade_id=self.provider.verify_callback(payload,signature)
        order.mark_paid(trade_id)
        return order
