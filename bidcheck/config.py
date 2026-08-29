from __future__ import annotations
import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    host:str='127.0.0.1'; port:int=8000; db_path:str='bidcheck.db'; max_body_bytes:int=10*1024*1024

def load_settings()->Settings:
    return Settings(os.getenv('BIDCHECK_HOST','127.0.0.1'),int(os.getenv('BIDCHECK_PORT','8000')),os.getenv('BIDCHECK_DB','bidcheck.db'),int(os.getenv('BIDCHECK_MAX_BODY','10485760')))
