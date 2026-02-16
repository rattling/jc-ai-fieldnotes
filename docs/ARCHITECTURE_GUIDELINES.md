# Architecture Guidelines for Experiments

This repo uses a pragmatic clean architecture style:
- domain logic stays isolated from infrastructure details
- adapters handle IO boundaries
- orchestration is explicit and testable
- design depth stays proportional to experiment scope

These guidelines apply to all CODED experiments.

## Architectural intent
- Preserve clarity over abstraction-heavy patterns.
- Keep the system easy to inspect, run, and evolve.
- Support fair A/B comparison when experiments evaluate design choices.

## Recommended module shape
Use this as a default, not a rigid rule:

- `domain/`: entities, value objects, domain rules, decision logic
- `application/`: use-cases/orchestration, ports, policies
- `adapters/`: external interfaces (LLM providers, storage, retrieval, APIs)
- `interface/` or `entrypoints/`: CLI, scripts, runners
- `eval/`: metrics, harness, reporting

A small experiment can collapse layers while preserving boundary intent.

## Dependency rule
Dependencies point inward:
- `interface -> application -> domain`
- `adapters -> application` via ports/contracts
- domain has no dependency on adapters

## Technology choices (default baseline)
- Python 3.11
- `uv` for environment/package workflows
- `pytest` for tests
- `ruff` for linting/format checks
- `pydantic` for schema boundaries where structured IO is required

Add heavier frameworks only when the experiment needs them.

## Testing and evals
Treat `pytest` and LLM evals as complementary, not interchangeable.

- `pytest` covers deterministic correctness: domain rules, schema checks, policies, adapters, retries.
- LLM eval harness covers behavioral quality on corpus runs: classification/routing quality, escalation quality, missing-field detection, latency/cost and failure slices.

Minimum expectation for LLM experiments:
1. unit/integration checks in `pytest`
2. offline replay eval against fixed dataset snapshot
3. run artifact capture (outputs + metrics) for A/B comparison over time

`pytest` alone is not sufficient for model-behavior evaluation.

## Framework policy (LangChain/LangGraph)
Default stance: start with plain Python orchestration and explicit adapters.

Adopt LangChain/LangGraph only when one or more are true:
- orchestration complexity is obscuring intent in custom code
- graph checkpointing/resume/human-in-loop is required
- provider/tool abstractions are creating repetitive boilerplate

If adopted, keep domain/application boundaries unchanged and treat framework code as adapter/orchestration infrastructure.

## Architectural invariants
Maintain these through build:
1. Domain rules are framework-agnostic.
2. All external side effects are behind adapters.
3. Input/output payloads crossing boundaries are schema-validated.
4. Orchestration paths are observable (structured logs/events).
5. Evaluation harness can replay runs deterministically where possible.
6. A and B designs share the same dataset and output schema for fair comparison.

## What to document for each experiment
Keep this lightweight but complete:
- purpose and scope boundary
- key architectural decisions and alternatives considered
- component diagram (static structure)
- sequence diagram(s) for primary execution path(s)
- state diagram if lifecycle or escalation states matter
- risks and failure modes
- measurable acceptance criteria and invariants

## ADR-lite format (recommended)
For each major decision, capture:
- **Context**: what pressure or trade-off exists
- **Decision**: chosen approach
- **Status**: proposed / accepted / superseded
- **Consequences**: benefits, costs, and follow-up actions

## Scaling guidance
Prefer adding structure in this order:
1. improve naming and module boundaries
2. add explicit ports/contracts
3. add adapter split and policy modules
4. add framework-specific orchestration only when justified

Avoid introducing architecture that the current experiment cannot validate.
