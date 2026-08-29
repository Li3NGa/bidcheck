from __future__ import annotations
from datetime import datetime

def markdown_report(project_id:str,result:dict)->str:
    summary=result.get('summary',{})
    lines=['# BidCheck 审计报告','',f'- 项目：`{project_id}`',f'- 生成时间：{datetime.now().isoformat(timespec="seconds")}',f'- 总要求：{summary.get("total",0)}',f'- 严重：{summary.get("critical",0)}',f'- 高风险：{summary.get("high",0)}',f'- 待复核：{summary.get("review",0)}','', '| 要求 | 风险级别 | 类型 | 页码 | 响应摘录 |','|---|---|---|---:|---|']
    for item in result.get('items',[]):
        excerpt=str(item.get('response_excerpt','')).replace('|','/').replace('\n',' ')
        lines.append(f"| {item.get('title','')} | {item.get('level','')} | {item.get('requirement_type','')} | {item.get('page') or ''} | {excerpt} |")
    return '\n'.join(lines)+'\n'
