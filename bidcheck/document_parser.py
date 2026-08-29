from __future__ import annotations
from pathlib import Path

class DocumentParseError(ValueError): pass

def extract_text(path:str|Path)->str:
    p=Path(path)
    if not p.exists(): raise DocumentParseError('document not found')
    suffix=p.suffix.lower()
    if suffix=='.txt': return p.read_text(encoding='utf-8')
    if suffix=='.pdf': return _pdf(p)
    if suffix=='.docx': return _docx(p)
    raise DocumentParseError(f'unsupported document type: {suffix}')

def _pdf(path:Path)->str:
    try:
        from pypdf import PdfReader
    except ImportError as exc: raise DocumentParseError('PDF support requires pypdf') from exc
    return '\n'.join(page.extract_text() or '' for page in PdfReader(str(path)).pages).strip()

def _docx(path:Path)->str:
    try:
        from docx import Document
    except ImportError as exc: raise DocumentParseError('DOCX support requires python-docx') from exc
    return '\n'.join(p.text for p in Document(str(path)).paragraphs if p.text).strip()
