from __future__ import annotations

from agents_vs_workflows.triage.schemas import DocType, Priority

REQUIRED_FIELDS_BY_DOC_TYPE: dict[DocType, tuple[str, ...]] = {
    "incident_report": ("service", "region", "request_id_examples"),
    "access_request": ("requested_role", "justification", "approval_reference"),
    "security_questionnaire": ("framework", "required_due_date"),
    "billing_dispute": ("issue_type", "invoice_id"),
    "feature_request": ("product_area", "business_justification"),
}

QUEUE_BY_DOC_TYPE: dict[DocType, str] = {
    "incident_report": "support_incident",
    "access_request": "security_access",
    "security_questionnaire": "compliance_ops",
    "billing_dispute": "billing_ops",
    "feature_request": "product_feedback",
}


def find_required_missing_fields(doc_type: DocType, metadata: dict[str, object]) -> list[str]:
    required = REQUIRED_FIELDS_BY_DOC_TYPE[doc_type]
    return [field for field in required if field not in metadata]


def recommend_queue(doc_type: DocType) -> str:
    return QUEUE_BY_DOC_TYPE[doc_type]


def should_escalate(
    doc_type: DocType,
    customer_tier: str | None,
    missing_fields: list[str],
    priority: Priority,
) -> tuple[bool, str | None]:
    if doc_type == "access_request" and customer_tier == "enterprise":
        return True, "Privileged access request for regulated/high-tier account"

    if doc_type == "incident_report" and "request_id_examples" in missing_fields and priority == "P1":
        return True, "Potential production incident with incomplete diagnostic evidence"

    if len(missing_fields) >= 2:
        return True, "Multiple required fields missing for safe automated triage"

    return False, None