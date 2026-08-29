from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from datetime import datetime,timezone

class Plan(str,Enum): FREE='free'; PRO='pro'; TEAM='team'

LIMITS={Plan.FREE:{'audits':3,'documents':10},Plan.PRO:{'audits':100,'documents':500},Plan.TEAM:{'audits':1000,'documents':5000}}

@dataclass(frozen=True)
class Subscription:
    user_id:str
    plan:Plan=Plan.FREE
    active:bool=True
    expires_at:datetime|None=None

    def allows(self,feature:str,used:int)->bool:
        if not self.active:return False
        if self.expires_at and self.expires_at<=datetime.now(timezone.utc):return False
        return used<LIMITS[self.plan].get(feature,0)
