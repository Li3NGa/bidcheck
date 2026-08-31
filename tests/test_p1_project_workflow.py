from bidcheck.project import TenderProject, audit_project
from bidcheck.requirements import RequirementGraph, Requirement
from bidcheck.tenant import User

def test_project_audit_returns_decision_and_records():
    graph=RequirementGraph([Requirement('R1','资格','具有软件开发经验',mandatory=True)])
    project=TenderProject('P1','demo',graph,['我司具有软件开发经验'])
    result=audit_project(project)
    assert result['project_id']=='P1'
    assert result['summary']['total']==1
    assert len(result['records'])==1

def test_project_tenant_access_is_enforced():
    graph=RequirementGraph([])
    project=TenderProject('P1','demo',graph,tenant_id='tenant-a')
    user=User('u1','tenant-b')
    try: audit_project(project,user)
    except PermissionError: pass
    else: raise AssertionError('tenant boundary was not enforced')
