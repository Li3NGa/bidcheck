from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime,timezone

@dataclass(frozen=True)
class Health:
    status:str
    service:str
    version:str
    timestamp:str

def health(service:str='bidcheck',version:str='0.1.0')->dict:
    value=Health('ok',service,version,datetime.now(timezone.utc).isoformat())
    return {'status':value.status,'service':value.service,'version':value.version,'timestamp':value.timestamp}
