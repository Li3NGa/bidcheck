from bidcheck.document import DocumentPage,ParsedDocument
from bidcheck.requirement_extract import extract_requirements
from bidcheck.multi_document import aggregate_responses

def test_best_evidence_can_come_from_second_document():
    graph=extract_requirements(ParsedDocument('b.pdf','.pdf',[DocumentPage(2,'资格要求：投标人须具备建筑工程资质')]))
    bundles=aggregate_responses(graph,['我方声明参与投标','我方具备建筑工程资质，证明见附件'])
    assert bundles[0].best_status=='matched'
    assert '建筑工程资质' in bundles[0].best_excerpt
