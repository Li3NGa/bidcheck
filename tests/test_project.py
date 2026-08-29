from bidcheck.document import DocumentPage,ParsedDocument
from bidcheck.requirement_extract import extract_requirements
from bidcheck.project import TenderProject,audit_project

def test_project_audit_aggregates_documents():
    graph=extract_requirements(ParsedDocument('b.pdf','.pdf',[DocumentPage(1,'资格要求：投标人须具备建筑工程资质')]))
    p=TenderProject('P1','测试项目',graph,['我方参与投标'])
    result=audit_project(p)
    assert result['project_id']=='P1'
    assert result['summary']['decision']=='BLOCK'
