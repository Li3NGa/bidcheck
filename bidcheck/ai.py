from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class AIResult:
    text:str
    model:str

class AIProvider(Protocol):
    def generate(self,prompt:str,context:str='')->AIResult: ...

class DisabledAIProvider:
    def generate(self,prompt:str,context:str='')->AIResult:
        return AIResult('', 'disabled')
