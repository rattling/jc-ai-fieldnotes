from __future__ import annotations

from agents_vs_workflows.agent.pipeline import run_agentic


def _agent_input(**overrides):
    payload = {
        "doc_id": "DOC-AG-001",
        "channel": "email",
        "customer_id": "CUST-4321",
        "customer_tier": "enterprise",
        "region": "EU",
        "submitted_at": "2026-02-16T12:00:00Z",
        "doc_type_hint": "access request",
        "content": "Need temporary privileged admin access for contractor migration.",
        "metadata": {
            "requested_role": "admin",
            "justification": "migration",
            "approval_reference": "CHG-300",
        },
    }
    payload.update(overrides)
    return payload


def test_agent_runner_enforces_tool_allowlist_fail_closed():
    decision = run_agentic(
        _agent_input(),
        allowlist={"detect_doc_type"},
        max_tool_calls=6,
    )

    assert decision.escalate is True
    assert decision.escalation_reason is not None
    assert "allowlist" in decision.escalation_reason.lower()


def test_agent_runner_enforces_tool_budget_fail_closed():
    decision = run_agentic(_agent_input(), max_tool_calls=1)

    assert decision.escalate is True
    assert decision.escalation_reason is not None
    assert "max tool calls" in decision.escalation_reason.lower()


def test_agent_runner_dynamic_paths_differ_by_case_pattern():
    access_decision = run_agentic(_agent_input())
    incident_decision = run_agentic(
        _agent_input(
            doc_id="DOC-AG-002",
            customer_tier="growth",
            doc_type_hint="incident report",
            content="Production incident: latency and outage symptoms in api gateway.",
            metadata={"service": "api-gateway", "region": "EU", "request_id_examples": "req-1"},
        )
    )

    access_tools = [step for step in access_decision.decision_trace.steps if step.startswith("tool:")]
    incident_tools = [step for step in incident_decision.decision_trace.steps if step.startswith("tool:")]

    assert access_tools != incident_tools
    assert access_decision.decision_trace.mode == "agent"
    assert incident_decision.decision_trace.mode == "agent"


def test_agent_runner_integration_end_to_end_validates_output():
    decision = run_agentic(_agent_input(), max_tool_calls=6)

    assert decision.doc_id == "DOC-AG-001"
    assert decision.recommended_queue == "security_access"
    assert decision.decision_trace.tool_calls >= 1