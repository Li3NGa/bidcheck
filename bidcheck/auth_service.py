from __future__ import annotations
from .auth import PasswordRecord,hash_password,verify_password
from .session import SessionStore
from .tenant import User,create_tenant

class AuthService:
    def __init__(self,sessions:SessionStore|None=None): self.sessions=sessions or SessionStore()
    def register(self,email:str,password:str,tenant_name:str,user_id:str)->tuple[User,PasswordRecord,str]:
        tenant=create_tenant(tenant_name,user_id)
        user=User(user_id,email.strip().lower(),tenant.tenant_id)
        record=hash_password(password)
        token=self.sessions.create(user.user_id,user.tenant_id)
        return user,record,token
    def authenticate(self,user:User,record:PasswordRecord,password:str)->str:
        if not verify_password(password,record): raise PermissionError('invalid credentials')
        return self.sessions.create(user.user_id,user.tenant_id)
