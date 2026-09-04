from __future__ import annotations
from pathlib import Path
from uuid import uuid4

ALLOWED_SUFFIXES={'.pdf','.docx','.txt','.xlsx'}
DEFAULT_MAX_BYTES=10*1024*1024

class UploadError(ValueError): pass

def save_upload(data:bytes,filename:str,directory:str|Path='uploads',max_bytes:int=DEFAULT_MAX_BYTES)->str:
    if not filename or Path(filename).name!=filename: raise UploadError('invalid filename')
    suffix=Path(filename).suffix.lower()
    if suffix not in ALLOWED_SUFFIXES: raise UploadError('unsupported document type')
    if not data: raise UploadError('empty document')
    if len(data)>max_bytes: raise UploadError('document too large')
    root=Path(directory); root.mkdir(parents=True,exist_ok=True)
    target=root/(uuid4().hex+suffix); target.write_bytes(data); return str(target)
