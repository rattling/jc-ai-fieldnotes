from __future__ import annotations

from time import perf_counter

from pydantic import ValidationError

from agents_vs_workflows.triage.engine import (
	build_decision,
	build_fail_closed_decision,
	detect_doc_type,
	elapsed_ms_since,
)
from agents_vs_workflows.triage.schemas import TriageDecision, TriageInput
from agents_vs_workflows.triage.validation import validate_triage_decision


def run_workflow(triage_input: TriageInput | dict, max_retries: int = 1) -> TriageDecision:
	start_time = perf_counter()
	steps = ["parse_input", "classify_and_plan"]
	retry_count = 0

	parsed_input = triage_input if isinstance(triage_input, TriageInput) else TriageInput(**triage_input)
	force_failure = bool(parsed_input.metadata.get("_force_validation_failure", False))
	force_retry_once = bool(parsed_input.metadata.get("_force_retry_once", False))

	for attempt in range(max_retries + 1):
		retry_count = attempt
		use_hint = attempt == 0
		doc_type = detect_doc_type(
			parsed_input.content,
			parsed_input.doc_type_hint if use_hint else None,
		)

		steps.append(f"build_candidate_attempt_{attempt}")

		queue_override = "invalid_queue" if (force_failure or (force_retry_once and attempt == 0)) else None

		try:
			decision = build_decision(
				parsed_input,
				mode="workflow",
				doc_type=doc_type,
				steps=steps,
				tool_calls=0,
				retry_count=retry_count,
				elapsed_ms=elapsed_ms_since(start_time),
				model_name="heuristic-v1",
				confidence=0.78 if attempt == 0 else 0.86,
				rationale="Fixed workflow triage with bounded repair loop.",
				queue_override=queue_override,
			)
		except ValidationError:
			if attempt < max_retries:
				steps.append("bounded_repair_retry")
				continue
			return build_fail_closed_decision(
				parsed_input,
				mode="workflow",
				steps=steps + ["escalate_fail_closed"],
				tool_calls=0,
				retry_count=retry_count,
				elapsed_ms=elapsed_ms_since(start_time),
				failure_reason="Validation failure after bounded retries",
			)

		violations = validate_triage_decision(parsed_input, decision)
		if not violations:
			decision.decision_trace.retry_count = retry_count
			decision.decision_trace.elapsed_ms = elapsed_ms_since(start_time)
			return decision

		if attempt < max_retries:
			steps.append("bounded_repair_retry")
			continue

		return build_fail_closed_decision(
			parsed_input,
			mode="workflow",
			steps=steps + ["escalate_fail_closed"],
			tool_calls=0,
			retry_count=retry_count,
			elapsed_ms=elapsed_ms_since(start_time),
			failure_reason="Policy validation failure after bounded retries",
		)

	return build_fail_closed_decision(
		parsed_input,
		mode="workflow",
		steps=steps + ["unexpected_exit"],
		tool_calls=0,
		retry_count=retry_count,
		elapsed_ms=elapsed_ms_since(start_time),
		failure_reason="Unexpected workflow runner exit",
	)