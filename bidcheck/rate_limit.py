from __future__ import annotations
from dataclasses import dataclass,field
from time import monotonic

@dataclass
class FixedWindowLimiter:
    limit:int=60
    window_seconds:float=60.0
    _hits:dict[str,list[float]]=field(default_factory=dict)
    def allow(self,key:str)->bool:
        now=monotonic(); cutoff=now-self.window_seconds
        hits=[ts for ts in self._hits.get(key,[]) if ts>=cutoff]
        if len(hits)>=self.limit:
            self._hits[key]=hits
            return False
        hits.append(now); self._hits[key]=hits
        if len(self._hits)>10000:
            self._hits={k:v for k,v in self._hits.items() if v}
        return True
