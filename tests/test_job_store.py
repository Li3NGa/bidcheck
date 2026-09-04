from bidcheck.job_store import SQLiteJobStore

def test_job_store_round_trip(tmp_path):
    store = SQLiteJobStore(tmp_path / 'jobs.db')
    created = store.create('audit', {'project_id': 'p1'})
    assert created['status'] == 'queued'
    assert store.get(created['job_id'])['payload']['project_id'] == 'p1'
    done = store.update(created['job_id'], 'completed', {'project_id': 'p1', 'score': 92})
    assert done['status'] == 'completed'
    assert store.get(created['job_id'])['payload']['score'] == 92
