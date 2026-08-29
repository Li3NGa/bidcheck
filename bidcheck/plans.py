from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Plan:
    name:str
    daily_audits:int
    max_documents:int
    export_report:bool

FREE=Plan('free',3,1,False)
PRO=Plan('pro',50,20,True)
TEAM=Plan('team',500,100,True)
