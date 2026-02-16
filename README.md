# jc-ai-fieldnotes

Applied data science, ML, and AI systems work grounded in realistic decision workflows.

This repo is designed to go beyond pattern demos.
It focuses on how AI systems behave in context: with policy constraints, failure modes, trade-offs, and judgement calls that resemble real operating environments.

Focus: judgement, production realism, and system design.

## Why this repo

There are many examples of AI patterns in isolation. There are fewer examples that:
- anchor those patterns in realistic use cases,
- compare alternatives fairly,
- show guardrails and failure boundaries,
- and document what was learned in a way others can reuse.

This repository is meant to be that kind of working field guide.

## How this repo is organized

- **Use cases** hold realistic domain framing and reusable core code.
- **Experiments** under each use case test specific design choices (A/B style).
- **Findings** are recorded primarily at experiment level (to avoid duplicated or drifting summaries at repo root), with top-level links for navigation.

## Field Notes

- [Repository field notes (reader-friendly guide)](docs/FIELDNOTES.md)
- [Current detailed findings: agents_vs_workflows](use_cases/customer_doc_triage/experiments/agents_vs_workflows/docs/FIELDNOTES.md)

## Architecture

- [Architecture guidelines for all experiments](docs/ARCHITECTURE_GUIDELINES.md)

## Use Cases

| Use Case | Purpose | Current Experiments |
|----------|---------|---------------------|
| `customer_doc_triage` | Customer document triage and routing | `agents_vs_workflows` |

Use-case shared code for `customer_doc_triage` lives in `use_cases/customer_doc_triage/src/customer_doc_triage`, while experiment folders keep run-mode specifics, eval artifacts, and notebooks.

## Contributor Workflow

For use-case work, follow this promotion loop:
- Create or update an experiment under `use_cases/<use_case>/experiments/<experiment_name>`.
- Reuse and extend shared domain/runtime code in `use_cases/<use_case>/src/<package>`.
- Keep experiment-specific plans, notebooks, and eval outputs inside the experiment folder.
- Promote validated reusable logic into the use-case package; keep experiment wrappers thin.

## Experiments

| Name | Status | Type | Focus |
|------|--------|------|-------|
| use_cases/customer_doc_triage/experiments/agents_vs_workflows | ACTIVE | CODED | Agentic vs constrained workflows in document triage |
| experiments/tabular_baselines | TODO | CODED | Modern tabular ML vs deep tabular models |


## Setup

Run once from repo root:

```bash
./scripts/setup_repo.sh
```

This script will:
- scaffold the repo layout (if missing)
- create `.venv` with Python 3.11 via `uv`
- install core tooling (`ruff`, `pytest`, `hatchling`)
- install local packages in editable mode

Activate the environment:

```bash
source .venv/bin/activate
```