from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class IngestedDocument:
    name:str
    text:str
    size_bytes:int

class IngestError(ValueError): pass

def ingest_text(path:str|Path,max_bytes:int=5_000_000)->IngestedDocument:
    p=Path(path)
    if max_bytes<=0: raise ValueError('max_bytes must be positive')
    if not p.is_file(): raise IngestError('input file not found')
    size=p.stat().st_size
    if size>max_bytes: raise IngestError('input file exceeds size limit')
    try: text=p.read_text(encoding='utf-8')
    except UnicodeDecodeError as exc: raise IngestError('input must be UTF-8 text') from exc
    if not text.strip(): raise IngestError('input document is empty')
    return IngestedDocument(p.name,text,size)
