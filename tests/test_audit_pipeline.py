from bidcheck.document import DocumentPage,ParsedDocument
from bidcheck.requirement_extract import extract_requirements
from bidcheck.audit_pipeline import audit_tender,audit_summary

def test_audit_pipeline_blocks_missing_qualification():
    doc=ParsedDocument('b.pdf','.pdf',[DocumentPage(7,'资格要求：投标人须具备建筑工程资质')])
    records=audit_tender(extract_requirements(doc),'我方参与投标')
    assert audit_summary(records)['decision']=='BLOCK'
    assert records[0].requirement_page==7
