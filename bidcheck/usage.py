from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Usage:
    user_id:str
    audits:int=0
    documents:int=0

class UsageLimitError(PermissionError): pass

def consume_audit(usage:Usage,limit:int)->Usage:
    if usage.audits>=limit: raise UsageLimitError('audit quota exceeded')
    usage.audits+=1
    return usage
