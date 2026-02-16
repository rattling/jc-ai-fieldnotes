from __future__ import annotations

from typing import Any

from agents_vs_workflows.triage.engine import detect_doc_type
from agents_vs_workflows.triage.policies import find_required_missing_fields
from agents_vs_workflows.triage.schemas import DocType, TriageInput

TOOL_ALLOWLIST = {
	"detect_doc_type",
	"extract_metadata",
	"check_completeness",
	"lookup_policy_context",
	"risk_scan",
}


def available_tools() -> list[str]:
	return sorted(TOOL_ALLOWLIST)


def detect_doc_type_tool(triage_input: TriageInput) -> dict[str, Any]:
	doc_type = detect_doc_type(triage_input.content, triage_input.doc_type_hint)
	return {"doc_type": doc_type}


def extract_metadata_tool(triage_input: TriageInput) -> dict[str, Any]:
	return {"metadata_keys": sorted(triage_input.metadata.keys())}


def check_completeness_tool(triage_input: TriageInput, doc_type: DocType) -> dict[str, Any]:
	missing = find_required_missing_fields(doc_type=doc_type, metadata=triage_input.metadata)
	return {"required_missing_fields": missing}


def lookup_policy_context_tool(triage_input: TriageInput) -> dict[str, Any]:
	return {
		"customer_tier": triage_input.customer_tier,
		"region": triage_input.region,
		"requires_heightened_review": triage_input.customer_tier == "enterprise",
	}


def risk_scan_tool(triage_input: TriageInput) -> dict[str, Any]:
	content_lower = triage_input.content.lower()
	risk_tokens = [
		token
		for token in ("admin", "privileged", "contractor", "outage", "incident", "regulated")
		if token in content_lower
	]
	return {"risk_tokens": risk_tokens, "risk_score": len(risk_tokens)}