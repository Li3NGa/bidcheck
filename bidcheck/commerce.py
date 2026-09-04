from __future__ import annotations
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Protocol
import json
import sqlite3
from .orders import Order, OrderStatus
from .payment import PaymentProvider, PaymentRequest, PaymentSession, PaymentNotConfigured
from .plans import FREE, PRO, TEAM, Plan

PLAN_PRICES_CENTS={'free':0,'pro':990,'team':2990}
PLANS={'free':FREE,'pro':PRO,'team':TEAM}

class OrderRepository(Protocol):
    def save(self,order:Order)->None: ...
    def get(self,order_id:str)->Order|None: ...

class SQLiteOrderRepository:
    def __init__(self,path:str='bidcheck.db'):
        self.path=path
        with sqlite3.connect(path) as db:
            db.execute('CREATE TABLE IF NOT EXISTS orders (order_id TEXT PRIMARY KEY,user_id TEXT NOT NULL,plan TEXT NOT NULL,amount INTEGER NOT NULL,status TEXT NOT NULL,provider_trade_id TEXT,created_at TEXT NOT NULL)')
            db.execute('CREATE TABLE IF NOT EXISTS entitlements (user_id TEXT PRIMARY KEY,plan TEXT NOT NULL,activated_at TEXT NOT NULL,order_id TEXT NOT NULL)')
            db.commit()
    def save(self,order:Order)->None:
        created=order.created_at.isoformat() if order.created_at else datetime.now(timezone.utc).isoformat()
        with sqlite3.connect(self.path) as db:
            db.execute('INSERT OR REPLACE INTO orders(order_id,user_id,plan,amount,status,provider_trade_id,created_at) VALUES(?,?,?,?,?,?,?)',(order.order_id,order.user_id,order.plan,order.amount,order.status.value,order.provider_trade_id,created)); db.commit()
    def get(self,order_id:str)->Order|None:
        with sqlite3.connect(self.path) as db: row=db.execute('SELECT user_id,plan,amount,order_id,status,provider_trade_id,created_at FROM orders WHERE order_id=?',(order_id,)).fetchone()
        if not row:return None
        return Order(row[0],row[1],row[2],row[3],OrderStatus(row[4]),row[5],datetime.fromisoformat(row[6]))
    def activate(self,user_id:str,plan:str,order_id:str)->None:
        with sqlite3.connect(self.path) as db:
            db.execute('INSERT OR REPLACE INTO entitlements(user_id,plan,activated_at,order_id) VALUES(?,?,?,?)',(user_id,plan,datetime.now(timezone.utc).isoformat(),order_id)); db.commit()
    def entitlement(self,user_id:str)->dict|None:
        with sqlite3.connect(self.path) as db: row=db.execute('SELECT user_id,plan,activated_at,order_id FROM entitlements WHERE user_id=?',(user_id,)).fetchone()
        return {'user_id':row[0],'plan':row[1],'activated_at':row[2],'order_id':row[3]} if row else None

class CommerceService:
    def __init__(self,repo:SQLiteOrderRepository,provider:PaymentProvider): self.repo=repo; self.provider=provider
    def create_order(self,user_id:str,plan_name:str)->Order:
        if not user_id.strip(): raise ValueError('user_id is required')
        plan=PLANS.get(plan_name.lower())
        if plan is None or plan is FREE: raise ValueError('a paid plan is required')
        order=Order(user_id,plan.name,PLAN_PRICES_CENTS[plan.name]); self.repo.save(order); return order
    def checkout(self,order_id:str,notify_url:str)->PaymentSession:
        order=self.repo.get(order_id)
        if order is None: raise KeyError(order_id)
        if order.status is not OrderStatus.PENDING: raise ValueError('order is not payable')
        return self.provider.create_payment(PaymentRequest(order.order_id,order.amount,f'BidCheck {order.plan}',notify_url))
    def confirm(self,order_id:str,payload:bytes,signature:str)->dict:
        order=self.repo.get(order_id)
        if order is None: raise KeyError(order_id)
        if order.status is OrderStatus.PAID: return {'order_id':order.order_id,'status':'paid','plan':order.plan,'idempotent':True}
        trade_id=self.provider.verify_callback(payload,signature); order.mark_paid(trade_id); self.repo.save(order); self.repo.activate(order.user_id,order.plan,order.order_id)
        return {'order_id':order.order_id,'status':'paid','plan':order.plan,'provider_trade_id':trade_id}
    def entitlement(self,user_id:str)->dict:
        return self.repo.entitlement(user_id) or {'user_id':user_id,'plan':'free'}
