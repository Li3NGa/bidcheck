import json
from bidcheck.document import DocumentPage,ParsedDocument
from bidcheck.requirement_extract import extract_requirements
from bidcheck.report_export import export_report

def test_export_report_is_machine_readable():
    graph=extract_requirements(ParsedDocument('b.pdf','.pdf',[DocumentPage(4,'资格要求：投标人须具备建筑工程资质')]))
    payload=json.loads(export_report(graph,'我方参与投标'))
    assert payload['summary']['decision']=='BLOCK'
    assert payload['records'][0]['page']==4
