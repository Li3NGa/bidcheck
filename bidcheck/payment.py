from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class PaymentRequest:
    order_id:str
    amount:int
    description:str
    notify_url:str

@dataclass(frozen=True)
class PaymentSession:
    provider:str
    order_id:str
    checkout_url:str

class PaymentProvider(Protocol):
    name:str
    def create_payment(self,request:PaymentRequest)->PaymentSession: ...
    def verify_callback(self,payload:bytes,signature:str)->str: ...

class PaymentNotConfigured(RuntimeError): pass

class DisabledPaymentProvider:
    name='disabled'
    def create_payment(self,request:PaymentRequest)->PaymentSession:
        raise PaymentNotConfigured('payment provider is not configured')
    def verify_callback(self,payload:bytes,signature:str)->str:
        raise PaymentNotConfigured('payment provider is not configured')
