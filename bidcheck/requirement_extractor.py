from __future__ import annotations
import re
from .requirements import Requirement,RequirementGraph,RequirementType

_PATTERNS=((RequirementType.REJECTION,r'(?:否决|废标|无效投标)[：:](.+)'),(RequirementType.QUALIFICATION,r'(?:资格条件|资质要求)[：:](.+)'),(RequirementType.ATTACHMENT,r'(?:须附|附件|证明材料)[：:](.+)'),(RequirementType.DEADLINE,r'(?:截止时间|投标截止)[：:](.+)'))

def extract_requirements(text:str)->RequirementGraph:
    if not isinstance(text,str) or not text.strip(): raise ValueError('tender text is required')
    graph=RequirementGraph(); index=0
    for line in text.splitlines():
        line=line.strip()
        if not line: continue
        for kind,pattern in _PATTERNS:
            match=re.search(pattern,line,re.I)
            if match:
                index+=1; graph.add(Requirement(f'R{index:04d}',kind,match.group(1).strip(),line,None,True)); break
    return graph
