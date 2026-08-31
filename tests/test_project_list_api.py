from bidcheck.api import BidCheckService
from bidcheck.http_api import list_projects
from bidcheck.store import MemoryProjectRepository
from bidcheck.project import TenderProject
from bidcheck.requirements import RequirementGraph

def test_list_projects_returns_project_summaries():
    repo=MemoryProjectRepository(); service=BidCheckService(repo)
    repo.save(TenderProject('p1','项目一',RequirementGraph()))
    repo.save(TenderProject('p2','项目二',RequirementGraph()))
    result=list_projects(service)
    assert [item['project_id'] for item in result]==['p1','p2']
