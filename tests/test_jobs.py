from bidcheck.jobs import AuditJobRunner, SQLiteJobStore


def test_job_lifecycle_and_persistence(tmp_path):
    store = SQLiteJobStore(str(tmp_path / 'jobs.db'))
    job = store.create('p1')
    assert job.status == 'queued'

    done = AuditJobRunner(store, lambda project_id: {'project_id': project_id, 'risk': 2}).run(job.job_id)
    assert done.status == 'completed'
    assert done.result == {'project_id': 'p1', 'risk': 2}
    assert store.get(job.job_id).result == done.result


def test_job_failure_is_persisted(tmp_path):
    store = SQLiteJobStore(str(tmp_path / 'jobs.db'))
    job = store.create('p2')

    failed = AuditJobRunner(store, lambda _: (_ for _ in ()).throw(RuntimeError('boom'))).run(job.job_id)
    assert failed.status == 'failed'
    assert failed.error == 'boom'
