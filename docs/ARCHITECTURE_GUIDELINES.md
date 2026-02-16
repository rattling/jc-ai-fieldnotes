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
