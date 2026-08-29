from bidcheck.document import DocumentPage,ParsedDocument
from bidcheck.requirement_extract import extract_requirements
from bidcheck.response_map import map_responses

def test_response_mapping_distinguishes_missing_and_present():
    doc=ParsedDocument("b.pdf",".pdf",[DocumentPage(2,"资格要求：投标人须具备建筑工程施工总承包资质。")])
    graph=extract_requirements(doc)
    results=map_responses(graph,"我方具备建筑工程施工总承包资质。")
    assert results[0].status=="matched"
    results=map_responses(graph,"我方声明。")
    assert results[0].status=="unmatched"
