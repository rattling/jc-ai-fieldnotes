from __future__ import annotations

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from agents_vs_workflows.triage.policies import (
    find_required_missing_fields,
    recommend_queue,
    should_escalate,
)
from agents_vs_workflows.triage.schemas import DecisionTrace, TriageDecision, TriageInput
from agents_vs_workflows.triage.validation import validate_triage_decision


def _base_input(**overrides):
    payload = {
        "doc_id": "DOC-1001",
        "channel": "email",
        "customer_id": "CUST-1234",
        "customer_tier": "enterprise",
        "region": "EU",
        "submitted_at": datetime(2026, 2, 16, 12, 0, tzinfo=timezone.utc),
        "doc_type_hint": "access request",
        "content": "Please grant temporary admin access for migration window.",
        "metadata": {
            "requested_role": "admin",
            "justification": "migration support",
        },
    }
    payload.update(overrides)
    return TriageInput(**payload)


def _base_decision(**overrides):
    payload = {
        "doc_id": "DOC-1001",
        "doc_type": "access_request",
        "priority": "P1",
        "severity_score": 5,
        "recommended_queue": "security_access",
        "required_missing_fields": ["approval_reference"],
        "escalate": True,
        "escalation_reason": "Privileged access request for regulated/high-tier account",
        "confidence": 0.81,
        "rationale": "Enterprise privileged access request needs security oversight.",
        "decision_trace": DecisionTrace(
            mode="workflow",
            steps=["parse", "classify", "validate", "route"],
            retry_count=1,
            elapsed_ms=240,
            model_name="gpt-4.1-mini",
        ),
    }
    payload.update(overrides)
    return TriageDecision(**payload)


def test_triage_input_schema_validates_expected_payload():
    triage_input = _base_input()
    assert triage_input.doc_id == "DOC-1001"
    assert triage_input.metadata["requested_role"] == "admin"


def test_triage_decision_requires_escalation_reason_when_escalate_true():
    with pytest.raises(ValidationError):
        _base_decision(escalation_reason=None)


def test_output_schema_is_shared_for_both_modes():
    workflow_decision = _base_decision(
        decision_trace=DecisionTrace(mode="workflow", steps=["parse"], elapsed_ms=120)
    )
    agent_decision = _base_decision(
        decision_trace=DecisionTrace(mode="agent", steps=["plan", "tool", "decide"], tool_calls=2)
    )

    assert set(workflow_decision.model_dump().keys()) == set(agent_decision.model_dump().keys())


def test_required_missing_fields_policy_detects_missing_metadata():
    missing = find_required_missing_fields(
        doc_type="access_request",
        metadata={"requested_role": "admin"},
    )
    assert missing == ["justification", "approval_reference"]


def test_recommend_queue_policy_mapping():
    assert recommend_queue("security_questionnaire") == "compliance_ops"


def test_should_escalate_policy_for_enterprise_access_request():
    escalate, reason = should_escalate(
        doc_type="access_request",
        customer_tier="enterprise",
        missing_fields=["approval_reference"],
        priority="P1",
    )
    assert escalate is True
    assert reason == "Privileged access request for regulated/high-tier account"


def test_should_not_escalate_for_low_risk_feature_request():
    escalate, reason = should_escalate(
        doc_type="feature_request",
        customer_tier="standard",
        missing_fields=[],
        priority="P3",
    )
    assert escalate is False
    assert reason is None


def test_validate_triage_decision_no_violations_for_valid_case():
    triage_input = _base_input()
    decision = _base_decision()

    violations = validate_triage_decision(triage_input, decision)
    assert violations == []


def test_validate_triage_decision_reports_queue_and_missing_field_mismatch():
    triage_input = _base_input()
    decision = _base_decision(
        recommended_queue="billing_ops",
        required_missing_fields=[],
    )

    violations = validate_triage_decision(triage_input, decision)
    assert any("recommended_queue mismatch" in violation for violation in violations)
    assert any("required_missing_fields mismatch" in violation for violation in violations)