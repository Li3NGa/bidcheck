from __future__ import annotations
from dataclasses import asdict
from .auth import hash_password,verify_password
from .sqlite_auth import SQLiteAuthStore
from .tenant import create_tenant,User
from .session import SessionStore

class APIError(Exception):
    def __init__(self,status:int,message:str): self.status=status; self.message=message

class BidCheckAPI:
    """Framework-neutral application service; adapters can expose these methods over HTTP."""
    def __init__(self,store:SQLiteAuthStore): self.store=store
    def register(self,email:str,password:str,tenant_name:str,user_id:str)->dict:
        if not email.strip(): raise APIError(400,'email is required')
        if not tenant_name.strip(): raise APIError(400,'tenant name is required')
        tenant=create_tenant(tenant_name,user_id); user=User(user_id,email.strip().lower(),tenant.tenant_id)
        try:self.store.save_user(user,hash_password(password))
        except Exception as exc:
            if 'UNIQUE' in str(exc).upper(): raise APIError(409,'email already registered')
            raise
        return {'user_id':user.user_id,'tenant_id':user.tenant_id}
    def login(self,email:str,password:str)->dict:
        found=self.store.get_user(email)
        if not found: raise APIError(401,'invalid credentials')
        user,record=found
        if not verify_password(password,record): raise APIError(401,'invalid credentials')
        token=self.store.create_session(user)
        return {'access_token':token,'token_type':'Bearer','user_id':user.user_id,'tenant_id':user.tenant_id}
