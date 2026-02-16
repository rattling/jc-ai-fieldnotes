from __future__ import annotations

from agents_vs_workflows.triage.schemas import TriageInput


def plan(triage_input: TriageInput) -> list[str]:
	content = triage_input.content.lower()

	if any(token in content for token in ("admin", "contractor", "privileged", "regulated")):
		return [
			"detect_doc_type",
			"lookup_policy_context",
			"risk_scan",
			"check_completeness",
		]

	if any(token in content for token in ("incident", "latency", "outage", "error")):
		return [
			"detect_doc_type",
			"extract_metadata",
			"check_completeness",
			"risk_scan",
		]

	return [
		"detect_doc_type",
		"extract_metadata",
		"check_completeness",
	]