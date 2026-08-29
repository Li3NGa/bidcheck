from bidcheck.api import BidCheckService
from bidcheck.document import DocumentPage,ParsedDocument
from bidcheck.requirement_extract import extract_requirements
from bidcheck.project import TenderProject
from bidcheck.store import MemoryProjectRepository

def project():
    graph=extract_requirements(ParsedDocument('b.pdf','.pdf',[DocumentPage(1,'资格要求：投标人须具备建筑工程资质')]))
    return TenderProject('P1','demo',graph,['我方参与投标'])

def test_create_get_and_audit():
    service=BidCheckService(MemoryProjectRepository()); service.create_project(project())
    assert service.get_project('P1').name=='demo'
    assert service.audit('P1')['summary']['decision']=='BLOCK'
