from __future__ import annotations
import re
from .document import ParsedDocument
from .requirements import Requirement,RequirementGraph,RequirementType
_PATTERNS=[(RequirementType.REJECTION,("废标","无效投标","否决投标")),(RequirementType.QUALIFICATION,("资格条件","资格要求","资质要求")),(RequirementType.SCORING,("评分标准","评分办法","评审因素","评分项")),(RequirementType.TECHNICAL,("技术要求","技术参数","技术需求")),(RequirementType.COMMERCIAL,("商务要求","商务条款")),(RequirementType.PERSONNEL,("人员要求","项目负责人","人员配备")),(RequirementType.EXPERIENCE,("业绩要求","类似业绩","项目经验")),(RequirementType.ATTACHMENT,("附件","证明材料","证明文件")),(RequirementType.FORMAT,("格式要求","响应格式","签字盖章")),(RequirementType.DEADLINE,("截止时间","递交截止","投标截止"))]
def extract_requirements(document:ParsedDocument)->RequirementGraph:
    graph=RequirementGraph(); counter=0
    for page in document.pages:
        for kind,keywords in _PATTERNS:
            for keyword in keywords:
                for m in re.finditer(re.escape(keyword),page.text):
                    counter+=1; snippet=page.text[max(0,m.start()-80):min(len(page.text),m.end()+180)].replace("\n"," ").strip()
                    graph.add(Requirement(f"R{counter:05d}",kind,keyword,snippet,page.page_number,kind in {RequirementType.REJECTION,RequirementType.QUALIFICATION,RequirementType.DEADLINE},{"source":document.source_name,"page":page.page_number,"keyword":keyword}))
    return graph
