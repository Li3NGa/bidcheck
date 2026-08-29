from __future__ import annotations
import os
from .api import BidCheckService
from .sqlite_store import SQLiteProjectRepository

def build_service()->BidCheckService:
    return BidCheckService(SQLiteProjectRepository(os.getenv('BIDCHECK_DB','bidcheck.db')))
