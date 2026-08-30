from bidcheck.file_ingest import ingest_text,IngestError

def test_ingest_rejects_missing(tmp_path):
    try: ingest_text(tmp_path/'missing.txt')
    except IngestError as exc: assert 'not found' in str(exc)
    else: raise AssertionError('expected IngestError')

def test_ingest_rejects_empty(tmp_path):
    p=tmp_path/'empty.txt'; p.write_text('',encoding='utf-8')
    try: ingest_text(p)
    except IngestError as exc: assert 'empty' in str(exc)
    else: raise AssertionError('expected IngestError')

def test_ingest_rejects_oversize(tmp_path):
    p=tmp_path/'large.txt'; p.write_text('12345',encoding='utf-8')
    try: ingest_text(p,max_bytes=4)
    except IngestError as exc: assert 'size limit' in str(exc)
    else: raise AssertionError('expected IngestError')
