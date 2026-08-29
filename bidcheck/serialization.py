from __future__ import annotations
from dataclasses import asdict
from .requirements import Requirement,RequirementGraph,RequirementType

def graph_to_dict(graph: RequirementGraph)->dict:
    return {"requirements":[asdict(r)|{"type":r.type.value} for r in graph.requirements]}

def graph_from_dict(data:dict)->RequirementGraph:
    if not isinstance(data,dict) or not isinstance(data.get('requirements'),list): raise ValueError('invalid requirement graph')
    graph=RequirementGraph()
    for item in data['requirements']:
        graph.add(Requirement(id=str(item['id']),type=RequirementType(item['type']),title=str(item['title']),text=str(item['text']),page=item.get('page'),mandatory=bool(item.get('mandatory',False)),evidence=dict(item.get('evidence',{}))))
    return graph
