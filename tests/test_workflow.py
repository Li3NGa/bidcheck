from bidcheck.workflow import build_project_from_document

def test_build_project_from_text(tmp_path):
    p=tmp_path/'t.txt'; p.write_text('供应商必须具备有效资质\n普通说明',encoding='utf-8')
    project=build_project_from_document('p1','demo',p)
    assert project.requirement_graph is not None
    assert len(project.requirement_graph.requirements)==1
