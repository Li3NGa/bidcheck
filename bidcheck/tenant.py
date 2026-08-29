from __future__ import annotations
from dataclasses import dataclass
from uuid import uuid4

@dataclass(frozen=True)
class Tenant:
    tenant_id:str
    name:str
    owner_user_id:str

@dataclass(frozen=True)
class User:
    user_id:str
    email:str
    tenant_id:str

def create_tenant(name:str,owner_user_id:str)->Tenant:
    if not name.strip() or not owner_user_id.strip(): raise ValueError('tenant name and owner are required')
    return Tenant(uuid4().hex,name.strip(),owner_user_id)

def assert_tenant_access(user:User,tenant_id:str)->None:
    if user.tenant_id!=tenant_id: raise PermissionError('tenant access denied')
