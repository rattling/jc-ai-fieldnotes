from agents_vs_workflows.workflow.pipeline import run_workflow


def test_workflow_smoke():
    decision = run_workflow(
        {
            "doc_id": "DOC-SMOKE-001",
            "channel": "portal",
            "customer_id": "CUST-SMOKE",
            "customer_tier": "standard",
            "region": "EU",
            "submitted_at": "2026-02-16T12:00:00Z",
            "doc_type_hint": "feature request",
            "content": "Feature request to improve reporting dashboard filters.",
            "metadata": {
                "product_area": "reporting dashboard",
                "business_justification": "reduce analyst time",
            },
        }
    )
    assert decision.doc_id == "DOC-SMOKE-001"