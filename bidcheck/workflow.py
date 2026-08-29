from __future__ import annotations
from pathlib import Path
from .document_parser import extract_text
from .project import TenderProject
from .requirements import RequirementGraph,Requirement,RequirementType

KEYWORDS={
    RequirementType.QUALIFICATION:('资格','资质'),
    RequirementType.TECHNICAL:('技术','参数','性能'),
    RequirementType.COMMERCIAL:('报价','商务','付款'),
    RequirementType.EXPERIENCE:('业绩','经验'),
    RequirementType.PERSONNEL:('人员','项目经理'),
    RequirementType.ATTACHMENT:('附件','证明材料'),
    RequirementType.DEADLINE:('截止','开标时间','交付时间'),
}

def _classify(line:str)->RequirementType:
    for kind,words in KEYWORDS.items():
        if any(word in line for word in words): return kind
    return RequirementType.REJECTION

def build_project_from_document(project_id:str,name:str,path:str|Path)->TenderProject:
    text=extract_text(path)
    graph=RequirementGraph()
    for i,raw in enumerate(text.splitlines(),1):
        line=raw.strip()
        if not line: continue
        if any(k in line for k in ('必须','应当','资格','资质','要求','不得','截止')):
            kind=_classify(line)
            graph.add(Requirement(f'r{i}',kind,line,line,i,True))
    # The tender source is not a response document. Responses must be attached explicitly.
    return TenderProject(project_id,name,graph,[])
