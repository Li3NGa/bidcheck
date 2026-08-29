from bidcheck.requirements import Requirement,RequirementGraph,RequirementType
from bidcheck.serialization import graph_to_dict,graph_from_dict

def test_requirement_graph_round_trip():
    g=RequirementGraph(); g.add(Requirement('r1',RequirementType.QUALIFICATION,'资质','建筑资质',3,True,{'source':'p3'}))
    loaded=graph_from_dict(graph_to_dict(g))
    assert loaded.requirements[0].id=='r1' and loaded.requirements[0].type is RequirementType.QUALIFICATION
