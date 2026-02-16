# JC AI Fieldnotes

Applied data science, ML, and AI systems work grounded in realistic decision workflows.

This repo is designed to go beyond pattern demos.
It focuses on how AI systems behave in context: with policy constraints, failure modes, trade-offs, and judgement calls that resemble real operating environments.

Focus: judgement, production realism, and system design.

## Quick Start

After cloning, from repo root:

```bash
cp .env.example .env
# edit .env and set OPENAI_API_KEY

uv venv -p 3.11
uv pip install --python .venv/bin/python ruff pytest hatchling
uv pip install --python .venv/bin/python -e shared -e use_cases/customer_doc_triage -e use_cases/customer_doc_triage/experiments/agents_vs_workflows
source .venv/bin/activate
```

Current provider setup is OpenAI-only (`OPENAI_API_KEY`).

Verify everything is wired correctly by running the active coded experiment:

```bash
python use_cases/customer_doc_triage/experiments/agents_vs_workflows/scripts/run_agents_vs_workflows.py --mode both
```

Optional one-command bootstrap/recovery path:

```bash
./scripts/setup_repo.sh
./scripts/setup_repo.sh --scaffold
```

## Why this repo

There are many examples of AI patterns in isolation. There are fewer examples that:
- anchor those patterns in realistic use cases,
- compare alternatives fairly,
- show guardrails and failure boundaries,
- and document what was learned in a way others can reuse.

This repository is meant to be that kind of working field guide.

## Entry points

Read first:
- [Repository field notes](docs/FIELDNOTES.md)
- [Use case: customer_doc_triage](use_cases/customer_doc_triage/README.md)
- [Experiment: agents_vs_workflows](use_cases/customer_doc_triage/experiments/agents_vs_workflows/README.md)
- [Detailed findings: agents_vs_workflows](use_cases/customer_doc_triage/experiments/agents_vs_workflows/docs/FIELDNOTES.md)

## Use Cases

| Use Case | Purpose | Current Experiments |
|----------|---------|---------------------|
| `customer_doc_triage` | Customer document triage and routing | `agents_vs_workflows` |

Use-case shared code for `customer_doc_triage` lives in `use_cases/customer_doc_triage/src/customer_doc_triage`, while experiment folders keep run-mode specifics, eval artifacts, and notebooks.

## Experiments

| Name | Status | Type | Focus |
|------|--------|------|-------|
| use_cases/customer_doc_triage/experiments/agents_vs_workflows | ACTIVE | CODED | Agentic vs constrained workflows in document triage |

## How this repo is organized

- **Use cases** hold realistic domain framing and reusable core code.
- **Experiments** under each use case test specific hypotheses or design choices (A/B, iterative, or single-design).
- **Findings** are recorded primarily at experiment level (to avoid duplicated or drifting summaries at repo root), with top-level links for navigation.

## Architecture

- [Architecture guidelines for all experiments](docs/ARCHITECTURE_GUIDELINES.md)

## Contributor Workflow

For use-case work, follow this promotion loop:
- Create or update an experiment under `use_cases/<use_case>/experiments/<experiment_name>`.
- Reuse and extend shared domain/runtime code in `use_cases/<use_case>/src/<package>`.
- Keep experiment-specific plans, notebooks, and eval outputs inside the experiment folder.
- Promote validated reusable logic into the use-case package; keep experiment wrappers thin.


