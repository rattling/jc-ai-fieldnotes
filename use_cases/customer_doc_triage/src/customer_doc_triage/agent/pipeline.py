from __future__ import annotations

from time import perf_counter

from customer_doc_triage.agent.planner import plan
from customer_doc_triage.agent.tools import (
    TOOL_ALLOWLIST,
    check_completeness_tool,
    detect_doc_type_tool,
    extract_metadata_tool,
    lookup_policy_context_tool,
    risk_scan_tool,
)
from customer_doc_triage.triage.engine import (
    build_decision,
    build_fail_closed_decision,
    detect_doc_type,
    elapsed_ms_since,
)
from customer_doc_triage.triage.schemas import TriageDecision, TriageInput
from customer_doc_triage.triage.validation import validate_triage_decision


def run_agentic(
    triage_input: TriageInput | dict,
    *,
    allowlist: set[str] | None = None,
    max_tool_calls: int = 6,
    timeout_ms: int = 2_000,
) -> TriageDecision:
    start_time = perf_counter()
    parsed_input = triage_input if isinstance(triage_input, TriageInput) else TriageInput(**triage_input)
    effective_allowlist = allowlist or TOOL_ALLOWLIST

    steps = ["parse_input", "agent_plan_start"]
    planned_tools = plan(parsed_input)
    tool_calls = 0
    inferred_doc_type = detect_doc_type(parsed_input.content, parsed_input.doc_type_hint)
    _agent_context: dict[str, object] = {}

    for tool_name in planned_tools:
        if tool_name not in effective_allowlist:
            return build_fail_closed_decision(
                parsed_input,
                mode="agent",
                steps=steps + [f"guardrail_allowlist_block:{tool_name}"],
                tool_calls=tool_calls,
                retry_count=0,
                elapsed_ms=elapsed_ms_since(start_time),
                failure_reason=f"Guardrail violation: tool '{tool_name}' not in allowlist",
            )

        if tool_calls >= max_tool_calls:
            return build_fail_closed_decision(
                parsed_input,
                mode="agent",
                steps=steps + ["guardrail_tool_budget_exceeded"],
                tool_calls=tool_calls,
                retry_count=0,
                elapsed_ms=elapsed_ms_since(start_time),
                failure_reason="Guardrail violation: max tool calls exceeded",
            )

        if elapsed_ms_since(start_time) > timeout_ms:
            return build_fail_closed_decision(
                parsed_input,
                mode="agent",
                steps=steps + ["guardrail_timeout"],
                tool_calls=tool_calls,
                retry_count=0,
                elapsed_ms=elapsed_ms_since(start_time),
                failure_reason="Guardrail violation: agent timeout budget exceeded",
            )

        steps.append(f"tool:{tool_name}")

        if tool_name == "detect_doc_type":
            result = detect_doc_type_tool(parsed_input)
            inferred_doc_type = result["doc_type"]
            _agent_context[tool_name] = result
        elif tool_name == "extract_metadata":
            _agent_context[tool_name] = extract_metadata_tool(parsed_input)
        elif tool_name == "check_completeness":
            _agent_context[tool_name] = check_completeness_tool(parsed_input, inferred_doc_type)
        elif tool_name == "lookup_policy_context":
            _agent_context[tool_name] = lookup_policy_context_tool(parsed_input)
        elif tool_name == "risk_scan":
            _agent_context[tool_name] = risk_scan_tool(parsed_input)

        tool_calls += 1

    steps.append("assemble_candidate")
    decision = build_decision(
        parsed_input,
        mode="agent",
        doc_type=inferred_doc_type,
        steps=steps,
        tool_calls=tool_calls,
        retry_count=0,
        elapsed_ms=elapsed_ms_since(start_time),
        model_name="heuristic-agent-v1",
        confidence=0.84,
        rationale="Dynamic agentic triage with guardrailed tool orchestration.",
    )

    violations = validate_triage_decision(parsed_input, decision)
    if violations:
        return build_fail_closed_decision(
            parsed_input,
            mode="agent",
            steps=steps + ["final_validation_fail_closed"],
            tool_calls=tool_calls,
            retry_count=0,
            elapsed_ms=elapsed_ms_since(start_time),
            failure_reason="Final schema/policy validation failed",
        )

    decision.decision_trace.elapsed_ms = elapsed_ms_since(start_time)
    return decision
