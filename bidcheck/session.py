from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime,timezone,timedelta
import hashlib
import secrets

@dataclass(frozen=True)
class Session:
    user_id:str
    tenant_id:str
    expires_at:datetime

class SessionStore:
    def __init__(self,ttl_hours:int=24):
        if ttl_hours<=0: raise ValueError('ttl_hours must be positive')
        self.ttl=timedelta(hours=ttl_hours); self._items={}
    def create(self,user_id:str,tenant_id:str)->str:
        token=secrets.token_urlsafe(32)
        self._items[self._key(token)]=Session(user_id,tenant_id,datetime.now(timezone.utc)+self.ttl)
        return token
    def get(self,token:str)->Session|None:
        session=self._items.get(self._key(token))
        if session is None:return None
        if session.expires_at<=datetime.now(timezone.utc):
            self._items.pop(self._key(token),None); return None
        return session
    def revoke(self,token:str)->None:self._items.pop(self._key(token),None)
    @staticmethod
    def _key(token:str)->str:return hashlib.sha256(token.encode()).hexdigest()
