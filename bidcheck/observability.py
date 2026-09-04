from __future__ import annotations
import json,logging
from datetime import datetime,timezone

class JsonFormatter(logging.Formatter):
    def format(self,record:logging.LogRecord)->str:
        payload={'ts':datetime.now(timezone.utc).isoformat(),'level':record.levelname,'logger':record.name,'message':record.getMessage()}
        if record.exc_info: payload['exception']=self.formatException(record.exc_info)
        return json.dumps(payload,ensure_ascii=False)

def configure_logging(level:str='INFO')->None:
    root=logging.getLogger(); root.setLevel(getattr(logging,level.upper(),logging.INFO))
    if not root.handlers:
        handler=logging.StreamHandler(); handler.setFormatter(JsonFormatter()); root.addHandler(handler)
