# jc-ai-fieldnotes

Applied data science, ML and AI systems work.

These notes document experiments, implementation patterns, architectural trade-offs, and evaluation approaches across classical DS, ML and GenAI systems.

Focus: judgement, production realism, and system design.

## Field Notes

- [Repository field notes (reader-friendly guide)](docs/FIELDNOTES.md)

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

| Name | Type | Focus |
|------|------|-------|
| use_cases/customer_doc_triage/experiments/agents_vs_workflows | CODED | Agentic vs constrained workflows in document triage |
| tabular_baselines | CODED | Modern tabular ML vs deep tabular models |


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