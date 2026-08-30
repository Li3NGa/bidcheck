from __future__ import annotations
import base64, hashlib, secrets, sqlite3
from datetime import datetime, timezone, timedelta
from pathlib import Path
from .auth import PasswordRecord
from .tenant import User

class SQLiteAuthStore:
    def __init__(self,path:str|Path='bidcheck.db',ttl_hours:int=24):
        if ttl_hours<=0: raise ValueError('ttl_hours must be positive')
        self.path=str(path); self.ttl=timedelta(hours=ttl_hours)
        with sqlite3.connect(self.path) as db:
            db.execute('CREATE TABLE IF NOT EXISTS users (user_id TEXT PRIMARY KEY, email TEXT NOT NULL UNIQUE, tenant_id TEXT NOT NULL, salt BLOB NOT NULL, digest BLOB NOT NULL, rounds INTEGER NOT NULL)')
            db.execute('CREATE TABLE IF NOT EXISTS auth_sessions (token_hash TEXT PRIMARY KEY, user_id TEXT NOT NULL, tenant_id TEXT NOT NULL, expires_at TEXT NOT NULL)')
            db.commit()
    def save_user(self,user:User,record:PasswordRecord)->None:
        with sqlite3.connect(self.path) as db:
            db.execute('INSERT INTO users(user_id,email,tenant_id,salt,digest,rounds) VALUES(?,?,?,?,?,?)',(user.user_id,user.email,user.tenant_id,record.salt,record.digest,record.rounds)); db.commit()
    def get_user(self,email:str)->tuple[User,PasswordRecord]|None:
        with sqlite3.connect(self.path) as db: row=db.execute('SELECT user_id,email,tenant_id,salt,digest,rounds FROM users WHERE email=?',(email.strip().lower(),)).fetchone()
        if not row:return None
        return User(row[0],row[1],row[2]),PasswordRecord(row[3],row[4],row[5])
    def create_session(self,user:User)->str:
        token=secrets.token_urlsafe(32); expires=datetime.now(timezone.utc)+self.ttl
        with sqlite3.connect(self.path) as db:
            db.execute('INSERT INTO auth_sessions(token_hash,user_id,tenant_id,expires_at) VALUES(?,?,?,?)',(hashlib.sha256(token.encode()).hexdigest(),user.user_id,user.tenant_id,expires.isoformat())); db.commit()
        return token
    def get_session(self,token:str):
        key=hashlib.sha256(token.encode()).hexdigest()
        with sqlite3.connect(self.path) as db: row=db.execute('SELECT user_id,tenant_id,expires_at FROM auth_sessions WHERE token_hash=?',(key,)).fetchone()
        if not row:return None
        expires=datetime.fromisoformat(row[2])
        if expires<=datetime.now(timezone.utc):
            self.revoke(token); return None
        return {'user_id':row[0],'tenant_id':row[1],'expires_at':expires}
    def revoke(self,token:str)->None:
        with sqlite3.connect(self.path) as db: db.execute('DELETE FROM auth_sessions WHERE token_hash=?',(hashlib.sha256(token.encode()).hexdigest(),)); db.commit()
