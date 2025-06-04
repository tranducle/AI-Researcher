import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from slr_assistant.project import SLRProject, Study


def test_add_and_list(tmp_path):
    proj_path = tmp_path / "proj"
    project = SLRProject(proj_path)
    study = Study(title="Test", authors="A", abstract="B")
    project.add_study(study)
    studies = project.list_studies()
    project.close()
    assert len(studies) == 1
    assert studies[0].title == "Test"
