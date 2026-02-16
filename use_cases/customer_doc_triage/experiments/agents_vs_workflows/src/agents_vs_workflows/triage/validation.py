from __future__ import annotations

from agents_vs_workflows.triage.policies import (
    find_required_missing_fields,
    recommend_queue,
    should_escalate,
)
from agents_vs_workflows.triage.schemas import TriageDecision, TriageInput


def validate_triage_decision(triage_input: TriageInput, decision: TriageDecision) -> list[str]:
    violations: list[str] = []

    if triage_input.doc_id != decision.doc_id:
        violations.append("doc_id mismatch between input and decision")

    expected_queue = recommend_queue(decision.doc_type)
    if decision.recommended_queue != expected_queue:
        violations.append(
            f"recommended_queue mismatch: expected={expected_queue} got={decision.recommended_queue}"
        )

    expected_missing = set(find_required_missing_fields(decision.doc_type, triage_input.metadata))
    actual_missing = set(decision.required_missing_fields)
    if expected_missing != actual_missing:
        violations.append(
            "required_missing_fields mismatch: "
            f"expected={sorted(expected_missing)} got={sorted(actual_missing)}"
        )

    should_escalate_flag, escalation_reason = should_escalate(
        doc_type=decision.doc_type,
        customer_tier=triage_input.customer_tier,
        missing_fields=decision.required_missing_fields,
        priority=decision.priority,
    )
    if should_escalate_flag and not decision.escalate:
        violations.append("decision must escalate per policy")
    if should_escalate_flag and decision.escalation_reason != escalation_reason:
        violations.append("escalation_reason mismatch with policy")

    return violations


def assert_valid_triage_decision(triage_input: TriageInput, decision: TriageDecision) -> None:
    violations = validate_triage_decision(triage_input=triage_input, decision=decision)
    if violations:
        raise ValueError("; ".join(violations))