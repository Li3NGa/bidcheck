from __future__ import annotations
from dataclasses import dataclass
from datetime import date

@dataclass
class UsageLimit:
    daily_audits:int=3
    audits_today:int=0
    day:date=date.today()

    def consume_audit(self)->None:
        today=date.today()
        if self.day!=today:self.day=today; self.audits_today=0
        if self.audits_today>=self.daily_audits:raise PermissionError('daily audit limit reached')
        self.audits_today+=1
