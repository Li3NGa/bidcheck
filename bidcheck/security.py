from __future__ import annotations

MAGIC={'.pdf':b'%PDF-','.docx':b'PK\x03\x04'}

def validate_content(data:bytes,suffix:str)->None:
    suffix=suffix.lower()
    if suffix in MAGIC and not data.startswith(MAGIC[suffix]):
        raise ValueError('file content does not match extension')
    if suffix=='.txt':
        try:data.decode('utf-8')
        except UnicodeDecodeError as exc:raise ValueError('invalid UTF-8 text') from exc
