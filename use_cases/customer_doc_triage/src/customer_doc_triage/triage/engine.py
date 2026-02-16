from __future__ import annotations

from time import perf_counter

from customer_doc_triage.triage.policies import (
    find_required_missing_fields,
    recommend_queue,
    should_escalate,
)
from customer_doc_triage.triage.schemas import DecisionTrace, DocType, TriageDecision, TriageInput

DOC_TYPE_KEYWORDS: dict[DocType, tuple[str, ...]] = {
    "incident_report": ("incident", "latency", "outage", "error rate", "request ids"),
    "access_request": ("access", "admin", "permission", "contractor", "privileged"),
    "security_questionnaire": ("security questionnaire", "soc2", "iso27001", "hipaa", "gdpr"),
    "billing_dispute": ("invoice", "billing", "charge", "overage", "tax"),
    "feature_request": ("feature request", "enhancement", "improve", "would like", "roadmap"),
}


def detect_doc_type(content: str, doc_type_hint: str | None = None) -> DocType:
    normalized_hint = (doc_type_hint or "").strip().lower().replace(" ", "_")
    if normalized_hint in DOC_TYPE_KEYWORDS:
        return normalized_hint  # type: ignore[return-value]

    content_lower = content.lower()
    best_doc_type: DocType = "feature_request"
    best_score = -1

    for doc_type, keywords in DOC_TYPE_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in content_lower)
        if score > best_score:
            best_doc_type = doc_type
            best_score = score

    return best_doc_type


def infer_priority(doc_type: DocType, customer_tier: str | None, missing_fields: list[str]) -> tuple[str, int]:
    base_priority_by_doc_type = {
        "incident_report": "P1",
        "access_request": "P2",
        "security_questionnaire": "P2",
        "billing_dispute": "P2",
        "feature_request": "P3",
    }

    priority = base_priority_by_doc_type[doc_type]
    if customer_tier == "enterprise" and priority == "P2":
        priority = "P1"
    if doc_type == "incident_report" and "request_id_examples" in missing_fields:
        priority = "P1"

    severity_by_priority = {"P1": 5, "P2": 3, "P3": 2}
    return priority, severity_by_priority[priority]


def build_decision(
    triage_input: TriageInput,
    *,
    mode: str,
    doc_type: DocType,
    steps: list[str],
    tool_calls: int,
    retry_count: int,
    elapsed_ms: int,
    model_name: str,
    confidence: float,
    rationale: str,
    doc_id_override: str | None = None,
    queue_override: str | None = None,
) -> TriageDecision:
    missing_fields = find_required_missing_fields(doc_type=doc_type, metadata=triage_input.metadata)
    priority, severity = infer_priority(doc_type, triage_input.customer_tier, missing_fields)
    queue = queue_override or recommend_queue(doc_type)
    escalate, escalation_reason = should_escalate(
        doc_type=doc_type,
        customer_tier=triage_input.customer_tier,
        missing_fields=missing_fields,
        priority=priority,
    )

    return TriageDecision(
        doc_id=doc_id_override or triage_input.doc_id,
        doc_type=doc_type,
        priority=priority,
        severity_score=severity,
        recommended_queue=queue,
        required_missing_fields=missing_fields,
        escalate=escalate,
        escalation_reason=escalation_reason,
        confidence=confidence,
        rationale=rationale,
        decision_trace=DecisionTrace(
            mode=mode,  # type: ignore[arg-type]
            steps=steps,
            tool_calls=tool_calls,
            retry_count=retry_count,
            elapsed_ms=elapsed_ms,
            model_name=model_name,
        ),
    )


def build_fail_closed_decision(
    triage_input: TriageInput,
    *,
    mode: str,
    steps: list[str],
    tool_calls: int,
    retry_count: int,
    elapsed_ms: int,
    failure_reason: str,
) -> TriageDecision:
    doc_type = detect_doc_type(triage_input.content, triage_input.doc_type_hint)
    missing_fields = find_required_missing_fields(doc_type=doc_type, metadata=triage_input.metadata)
    priority, severity = infer_priority(doc_type, triage_input.customer_tier, missing_fields)

    return TriageDecision(
        doc_id=triage_input.doc_id,
        doc_type=doc_type,
        priority=priority,
        severity_score=severity,
        recommended_queue=recommend_queue(doc_type),
        required_missing_fields=missing_fields,
        escalate=True,
        escalation_reason=failure_reason,
        confidence=0.0,
        rationale="Fail-closed escalation due to runner validation/guardrail failure.",
        decision_trace=DecisionTrace(
            mode=mode,  # type: ignore[arg-type]
            steps=steps,
            tool_calls=tool_calls,
            retry_count=retry_count,
            elapsed_ms=elapsed_ms,
            model_name="heuristic-v1",
        ),
    )


def elapsed_ms_since(start: float) -> int:
    return max(1, int((perf_counter() - start) * 1000))