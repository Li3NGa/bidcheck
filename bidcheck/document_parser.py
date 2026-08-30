from __future__ import annotations
from pathlib import Path

class DocumentParseError(ValueError): pass

SUPPORTED={'.txt','.pdf','.docx','.xlsx'}

def extract_text(path:str|Path,max_bytes:int=20_000_000)->str:
    p=Path(path)
    if not p.is_file(): raise DocumentParseError('document not found')
    if max_bytes<=0: raise ValueError('max_bytes must be positive')
    if p.stat().st_size>max_bytes: raise DocumentParseError('document exceeds size limit')
    suffix=p.suffix.lower()
    if suffix not in SUPPORTED: raise DocumentParseError(f'unsupported document type: {suffix}')
    if suffix=='.txt': text=p.read_text(encoding='utf-8')
    elif suffix=='.pdf': text=_pdf(p)
    elif suffix=='.docx': text=_docx(p)
    else: text=_xlsx(p)
    if not text.strip(): raise DocumentParseError('document is empty')
    return text

def _pdf(path:Path)->str:
    try:
        from pypdf import PdfReader
        return '\n'.join(page.extract_text() or '' for page in PdfReader(str(path)).pages).strip()
    except Exception as exc: raise DocumentParseError('failed to parse PDF') from exc

def _docx(path:Path)->str:
    try:
        from docx import Document
        return '\n'.join(p.text for p in Document(str(path)).paragraphs if p.text).strip()
    except Exception as exc: raise DocumentParseError('failed to parse DOCX') from exc

def _xlsx(path:Path)->str:
    try:
        from openpyxl import load_workbook
        wb=load_workbook(str(path),read_only=True,data_only=True)
        return '\n'.join(' | '.join('' if v is None else str(v) for v in row) for ws in wb.worksheets for row in ws.iter_rows(values_only=True)).strip()
    except Exception as exc: raise DocumentParseError('failed to parse XLSX') from exc
