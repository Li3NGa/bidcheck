from bidcheck.document import DocumentPage,ParsedDocument
from bidcheck.requirement_extract import extract_requirements
from bidcheck.radar import build_radar

def test_radar_blocks_unmatched_mandatory_requirement():
    doc=ParsedDocument("b.pdf",".pdf",[DocumentPage(3,"资格要求：投标人须具备建筑工程资质")])
    graph=extract_requirements(doc)
    radar=build_radar(graph,"我方声明参与投标")
    assert radar["decision"]=="BLOCK"
    assert radar["items"][0]["page"]==3
