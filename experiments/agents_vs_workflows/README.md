# agents_vs_workflows

Type: CODED
Depth: MVP

## Purpose
Compare two LLM-powered approaches for customer document triage in a realistic support workflow:
- **A: workflow-constrained LLM** (bounded role inside deterministic orchestration)
- **B: agentic LLM** (model chooses tools/actions under guardrails)

Goal: isolate when agentic behavior adds meaningful value over constrained workflows.

## Descriptive docs (start here)
- [Fieldnotes](docs/FIELDNOTES.md)
- [Domain, company, and use case](docs/01_domain_and_use_case.md)
- [As-is process and BPMs](docs/02_as_is_process.md)
- [Problem statement](docs/03_problem_statement.md)
- [LLM replacement + Design A/B + ADR](docs/04_target_designs_and_adr.md)
- [Synthetic data plan](docs/05_synthetic_data_plan.md)

## Synthetic corpus generation
Generate reproducible dataset artifacts:

```bash
python experiments/agents_vs_workflows/scripts/generate_synthetic_data.py --count 200 --seed 42
```

Outputs:
- `data/samples.jsonl` (inputs)
- `data/gold.jsonl` (expected labels)

## What comes next
1. Create synthetic customer documents in `data/`.
2. Build shared ingestion/schema/eval components.
3. Implement swappable runners for A and B.
4. Evaluate quality, latency, and rework outcomes.

## Scope boundaries
- Same input corpus for A and B.
- Same output schema for both designs.
- Human escalation path remains available in both.