# jc-ai-fieldnotes

Applied data science, ML and AI systems work.

These notes document experiments, implementation patterns, architectural trade-offs, and evaluation approaches across classical DS, ML and GenAI systems.

Focus: judgement, production realism, and system design.

## Architecture

- [Architecture guidelines for all experiments](docs/ARCHITECTURE_GUIDELINES.md)

## Experiments

| Name | Type | Focus |
|------|------|-------|
| agents_vs_workflows | CODED | Agentic vs constrained workflows in document triage |
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