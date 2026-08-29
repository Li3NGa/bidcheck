from bidcheck.store import MemoryProjectRepository
from bidcheck.project import TenderProject

def test_project_repository_round_trip():
    repo=MemoryProjectRepository()
    project=TenderProject('P1','demo',None)
    repo.save(project)
    assert repo.get('P1') is project
    assert repo.get('missing') is None
