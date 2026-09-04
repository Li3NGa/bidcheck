import base64
from pathlib import Path
from bidcheck.api import BidCheckService
from bidcheck.store import MemoryProjectRepository
from bidcheck.upload_api import create_project_from_upload,attach_response_from_upload

def enc(text:str)->str:return base64.b64encode(text.encode()).decode()

def test_upload_creates_project_and_attaches_response(tmp_path:Path):
    service=BidCheckService(MemoryProjectRepository())
    tender={'project_id':'P1','name':'demo','filename':'tender.txt','content_base64':enc('资格要求：具有软件开发经验')}
    project=create_project_from_upload(service,tender,tmp_path)
    assert project['project_id']=='P1'
    response={'filename':'response.txt','content_base64':enc('我司具有软件开发经验')}
    attached=attach_response_from_upload(service,'P1',response,tmp_path)
    assert attached['response_documents']==1
