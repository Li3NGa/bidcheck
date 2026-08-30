from pathlib import Path
from bidcheck.file_ingest import IngestError, ingest_text

def test_ingest_txt(tmp_path: Path):
    p=tmp_path/'a.txt'; p.write_text('资格要求：具有软件开发经验',encoding='utf-8')
    doc=ingest_text(p)
    assert doc.text.startswith('资格要求') and doc.media_type=='text/plain'

def test_ingest_rejects_oversize(tmp_path: Path):
    p=tmp_path/'a.txt'; p.write_text('abcdef',encoding='utf-8')
    try: ingest_text(p,max_bytes=2)
    except IngestError as exc: assert 'size' in str(exc)
    else: raise AssertionError('expected size error')
