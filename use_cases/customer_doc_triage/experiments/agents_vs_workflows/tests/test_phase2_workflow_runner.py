from __future__ import annotations

from agents_vs_workflows.workflow.pipeline import run_workflow


def _sample_input(**overrides):
    payload = {
        "doc_id": "DOC-WF-001",
        "channel": "email",
        "customer_id": "CUST-1234",
        "customer_tier": "enterprise",
        "region": "EU",
        "submitted_at": "2026-02-16T12:00:00Z",
        "doc_type_hint": "access request",
        "content": "Need temporary admin access for contractor during migration.",
        "metadata": {
            "requested_role": "admin",
            "justification": "migration window",
            "approval_reference": "CHG-100",
        },
    }
    payload.update(overrides)
    return payload


def test_workflow_runner_retries_once_and_returns_valid_decision():
    metadata = {
        "requested_role": "admin",
        "justification": "migration window",
        "approval_reference": "CHG-100",
        "_force_retry_once": True,
    }
    decision = run_workflow(_sample_input(metadata=metadata), max_retries=1)

    assert decision.doc_id == "DOC-WF-001"
    assert decision.decision_trace.mode == "workflow"
    assert decision.decision_trace.retry_count == 1
    assert "bounded_repair_retry" in decision.decision_trace.steps


def test_workflow_runner_fails_closed_after_validation_failure():
    payload = _sample_input(metadata={"_force_validation_failure": True})
    decision = run_workflow(payload, max_retries=1)

    assert decision.escalate is True
    assert decision.escalation_reason is not None
    assert "failure" in decision.escalation_reason.lower()


def test_workflow_runner_integration_subset_executes_end_to_end():
    fixture_docs = [
        _sample_input(doc_id="DOC-WF-INT-1"),
        _sample_input(
            doc_id="DOC-WF-INT-2",
            content="Production incident with latency spike in api-gateway.",
            doc_type_hint="incident report",
            metadata={"service": "api-gateway", "region": "EU", "request_id_examples": "abc-123"},
        ),
    ]

    decisions = [run_workflow(doc, max_retries=1) for doc in fixture_docs]
    assert len(decisions) == 2
    assert all(decision.doc_id.startswith("DOC-WF-INT") for decision in decisions)