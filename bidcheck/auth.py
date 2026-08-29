from __future__ import annotations
from dataclasses import dataclass
import hashlib
import hmac
import secrets

@dataclass(frozen=True)
class PasswordRecord:
    salt: bytes
    digest: bytes
    rounds: int = 310000

def hash_password(password:str, rounds:int=310000)->PasswordRecord:
    if len(password)<8: raise ValueError('password must be at least 8 characters')
    salt=secrets.token_bytes(16)
    digest=hashlib.pbkdf2_hmac('sha256',password.encode('utf-8'),salt,rounds)
    return PasswordRecord(salt,digest,rounds)

def verify_password(password:str,record:PasswordRecord)->bool:
    digest=hashlib.pbkdf2_hmac('sha256',password.encode('utf-8'),record.salt,record.rounds)
    return hmac.compare_digest(digest,record.digest)

def issue_session_token()->str:
    return secrets.token_urlsafe(32)
