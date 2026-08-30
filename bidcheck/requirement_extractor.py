from __future__ import annotations
import re
from .requirements import Requirement,RequirementGraph,RequirementType

_PATTERNS=(
 (RequirementType.REJECTION,r'(?:否决|废标|无效投标)[：:](.+)'),
 (RequirementType.QUALIFICATION,r'(?:资格条件|资质要求|资格要求)[：:](.+)'),
 (RequirementType.ATTACHMENT,r'(?:须附|附件|证明材料|提供材料)[：:](.+)'),
 (RequirementType.DEADLINE,r'(?:截止时间|投标截止|提交截止)[：:](.+)'),
 (RequirementType.TECHNICAL,r'(?:技术要求|技术参数|技术指标)[：:](.+)'),
 (RequirementType.COMMERCIAL,r'(?:商务要求|报价要求|价格要求)[：:](.+)'),
 (RequirementType.PERSONNEL,r'(?:人员要求|项目负责人)[：:](.+)'),
 (RequirementType.EXPERIENCE,r'(?:业绩要求|经验要求)[：:](.+)'),
 (RequirementType.FORMAT,r'(?:格式要求|文件格式)[：:](.+)'),
)

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
