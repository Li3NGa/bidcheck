from __future__ import annotations
from .session import SessionStore
from .tenant import User

class AuthenticationRequired(PermissionError): pass

def authenticate_bearer(authorization:str, sessions:SessionStore)->User:
    if not authorization.startswith('Bearer '):
        raise AuthenticationRequired('bearer token required')
    token=authorization[7:].strip()
    if not token: raise AuthenticationRequired('bearer token required')
    session=sessions.get(token)
    if session is None: raise AuthenticationRequired('invalid or expired session')
    return User(session.user_id,'',session.tenant_id)
