from __future__ import annotations
from pathlib import Path
from .document_parser import extract_text
from .project import TenderProject

def attach_response_document(project:TenderProject,path:str|Path,max_bytes:int=20_000_000)->TenderProject:
    text=extract_text(path,max_bytes)
    if not text.strip(): raise ValueError('response document contains no extractable text')
    value=str(path)
    if value not in project.response_documents: project.response_documents.append(value)
    return project
