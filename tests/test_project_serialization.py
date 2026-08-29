from bidcheck.project import TenderProject
from bidcheck.requirements import Requirement,RequirementGraph,RequirementType
from bidcheck.project_serialization import project_to_dict,project_from_dict

def test_project_round_trip():
    g=RequirementGraph(); g.add(Requirement('r1',RequirementType.QUALIFICATION,'资质','要求',2,True))
    p=TenderProject('p1','项目',g,['a.pdf']); q=project_from_dict(project_to_dict(p))
    assert q.project_id=='p1' and q.requirement_graph.requirements[0].id=='r1' and q.response_documents==['a.pdf']
