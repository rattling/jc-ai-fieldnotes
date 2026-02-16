# jc-ai-fieldnotes

Applied data science, ML and AI systems work.

These notes document experiments, implementation patterns, architectural trade-offs, and evaluation approaches across classical DS, ML and GenAI systems.

Focus: judgement, production realism, and system design.

## Architecture

- [Architecture guidelines for all experiments](docs/ARCHITECTURE_GUIDELINES.md)

## Use Cases

| Use Case | Purpose | Current Experiments |
|----------|---------|---------------------|
| `customer_doc_triage` | Customer document triage and routing | `agents_vs_workflows` |

Use-case shared code for `customer_doc_triage` lives in `use_cases/customer_doc_triage/src/customer_doc_triage`, while experiment folders keep run-mode specifics, eval artifacts, and notebooks.

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