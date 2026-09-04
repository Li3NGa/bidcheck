from pathlib import Path

from bidcheck.project import TenderProject, audit_project
from bidcheck.requirements import Requirement, RequirementGraph


def test_project_audit_parses_response_file(tmp_path: Path):
    response = tmp_path / "response.txt"
    response.write_text("我司具有软件开发经验", encoding="utf-8")
    graph = RequirementGraph([Requirement("R1", "资格", "具有软件开发经验", mandatory=True)])
    project = TenderProject("P-FILE", "file-demo", graph, [str(response)])

    result = audit_project(project)

    assert result["summary"]["total"] == 1
    assert len(result["records"]) == 1
