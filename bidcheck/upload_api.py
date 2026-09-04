from __future__ import annotations
from pathlib import Path
from typing import Any
import base64,binascii
from .api import BidCheckService
from .product_api import create_from_tender, attach_response
from .upload import save_upload, UploadError
from .http_api import APIError

def _save(payload:dict[str,Any],directory:str|Path,max_bytes:int)->str:
    if not isinstance(payload,dict) or not payload.get('filename') or not payload.get('content_base64'):
        raise APIError(400,'invalid_document','filename and content_base64 are required')
    try:data=base64.b64decode(str(payload['content_base64']),validate=True)
    except (binascii.Error,ValueError) as exc:raise APIError(400,'invalid_base64','content_base64 is invalid') from exc
    try:return save_upload(data,str(payload['filename']),directory,max_bytes)
    except UploadError as exc:raise APIError(400,'invalid_document',str(exc)) from exc

def create_project_from_upload(service:BidCheckService,payload:dict[str,Any],directory:str|Path='uploads',max_bytes:int=10_000_000)->dict:
    if not isinstance(payload,dict) or not payload.get('project_id') or not payload.get('name'):
        raise APIError(400,'invalid_project','project_id and name are required')
    path=_save(payload,directory,max_bytes)
    result=create_from_tender(service,str(payload['project_id']),str(payload['name']),path)
    return {**result,'tender_document':Path(path).name}

def attach_response_from_upload(service:BidCheckService,project_id:str,payload:dict[str,Any],directory:str|Path='uploads',max_bytes:int=10_000_000)->dict:
    path=_save(payload,directory,max_bytes)
    result=attach_response(service,project_id,path)
    return {**result,'response_document':Path(path).name}
