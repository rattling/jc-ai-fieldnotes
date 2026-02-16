from agents_vs_workflows.workflow.pipeline import run_workflow


def test_workflow_smoke():
    assert run_workflow()["status"] == "ok"