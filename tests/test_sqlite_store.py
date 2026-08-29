from bidcheck.sqlite_store import SQLiteProjectRepository
from bidcheck.project import TenderProject

def test_sqlite_round_trip(tmp_path):
    repo=SQLiteProjectRepository(tmp_path/'test.db')
    p=TenderProject('p1','demo',None,['doc'])
    repo.save(p); loaded=repo.get('p1')
    assert loaded is not None and loaded.name=='demo' and loaded.response_documents==['doc']
