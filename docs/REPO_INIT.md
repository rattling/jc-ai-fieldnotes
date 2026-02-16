# JC AI Fieldnotes — Monorepo (uv + Python 3.11) Setup

This doc describes a **single-venv monorepo** where each experiment is its **own installable Python package** (clean absolute imports, its own README, tests, and dependencies), while you still work from **one shared Python 3.11 virtual environment** at repo root.

The goal is to make this repo:
- **Legible to humans** (senior/architect signal)
- **Easy to run** (one venv, consistent commands)
- **Modular** (each experiment stands alone)
- **Scalable** (you can add many experiments without dependency chaos)

---

## Core design choices

### “Workspace” model (pragmatic)
- **One virtualenv at repo root** (Python 3.11).
- Each experiment has its own `pyproject.toml` with its own dependencies.
- You “workspace-install” by installing **each package editable** into the one root venv:
  - `uv pip install -e shared -e use_cases/customer_doc_triage/experiments/agents_vs_workflows ...`
- This produces a **single environment** containing the union of dependencies across installed packages, while preserving per-experiment packaging boundaries.

This is *functionally* a workspace even if we don’t rely on any specific uv “workspace” TOML schema that might change over time.

---

## Current repo structure

```text
jc-ai-fieldnotes/
  README.md
  pyproject.toml                  # root tooling config (ruff/pytest/mypy), optional dev deps
  uv.lock                         # optional: if you choose to lock from root later
  .python-version                 # 3.11.x (optional)
  .gitignore

  scripts/
    setup_repo.sh                 # idempotent bootstrap (scaffold + venv + editable installs)

  shared/
    README.md
    pyproject.toml
    src/
      shared/
        __init__.py
        logging.py                # optional shared logging helpers
        eval_utils.py             # optional shared eval helpers
    tests/

  use_cases/
    customer_doc_triage/
      experiments/
        agents_vs_workflows/
          README.md
          pyproject.toml
          src/
            agents_vs_workflows/
              __init__.py
              config.py
              workflow/
                __init__.py
                run.py
                pipeline.py
                schemas.py
              agent/
                __init__.py
                run.py
                tools.py
                planner.py
                schemas.py
              eval/
                __init__.py
                metrics.py
                report.py
          tests/
          data/
            samples.jsonl
            gold.jsonl

  experiments/
    tabular_baselines/
      README.md
      pyproject.toml
      src/
        tabular_baselines/
          __init__.py
      tests/
      data/
```

### Naming conventions
- Folder + package names: **snake_case** (e.g., `agents_vs_workflows`).
- Python package code always under `src/<package_name>/...`.
- Tests under `tests/` using `pytest`.
- Keep each experiment’s README very explicit:
  - **Type:** CODED or DESIGN
  - **Depth:** MVP / production-like / analysis-only
  - **How to run**
  - **What you learned**

---

## Root environment (uv + Python 3.11)

### Bootstrap everything (repo root)
```bash
./scripts/setup_repo.sh
```

This script will:
- scaffold missing folders/files for the baseline monorepo layout
- create `.venv` using Python 3.11 (`uv venv -p 3.11`)
- install core tooling (`ruff`, `pytest`, `hatchling`)
- install local packages editable (`shared`, `agents_vs_workflows`, `tabular_baselines`)

Activate after bootstrap:
- Linux/macOS:
  ```bash
  source .venv/bin/activate
  ```
- Windows (PowerShell):
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```

---

## Installing packages into the workspace venv

### Install shared + all experiments (editable)
From repo root:
```bash
uv pip install -e shared   -e use_cases/customer_doc_triage/experiments/agents_vs_workflows   -e experiments/tabular_baselines
```

This gives you:
- Absolute imports (clean): `from agents_vs_workflows.workflow.pipeline import ...`
- One environment to run everything
- Experiments remain independently installable (each has its own `pyproject.toml`)

### Running a module (example)
```bash
python -m agents_vs_workflows.workflow.run
python -m agents_vs_workflows.agent.run
python -m agents_vs_workflows.eval.report
```

---

## Minimal `pyproject.toml` templates

### Root `pyproject.toml` (tooling config only)
Keep root simple: it configures linters/test runner for the whole repo.

```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.pytest.ini_options]
testpaths = ["shared/tests", "experiments", "use_cases"]
addopts = "-q"
```

(You can add `mypy` config later.)

### Subproject `pyproject.toml` template (shared / each experiment)
Use PEP 621, with `src/` layout.

```toml
[project]
name = "agents-vs-workflows"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
  "pydantic>=2",
  "numpy",
  "pandas",
  "scikit-learn",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/agents_vs_workflows"]
```

Notes:
- `project.name` may contain hyphens; the **import package** remains `agents_vs_workflows`.
- Add GenAI libs only in the experiments that need them (e.g. `openai`, `langchain`, `langgraph`, etc.).

---

## Scripts

### `scripts/setup_repo.sh`
Purpose: one command to recreate the repo baseline after cloning.

Design notes:
- Safe to re-run (creates files only if missing, then re-installs deps)
- Keeps a single shared `.venv` at repo root
- Central place to update editable package install list when adding experiments

---

## Guidance for keeping it sane

### Dependency discipline
- Keep “shared” utilities minimal.
- Prefer experiment-local deps unless clearly reusable.
- If two experiments need the same helper, move it to `shared/`.

### CODED vs DESIGN flagging
In each experiment README, include:
- **Type:** CODED / DESIGN
- **What is implemented**
- **What is mocked**
- **How to run**
- **What to look at first**

### Testing expectation (lightweight but real)
Each CODED experiment should have at least:
- A smoke test that the pipeline runs on a tiny dataset
- A test asserting schema validity / output shape
- A regression test for a known failure mode (once you find one)

---

## “Agents vs Workflows” (first experiment) execution outline

Implement two runnable pipelines against the *same* dataset and schema:

1) **Workflow (constrained)**
- Bounded steps
- Schema validation
- Deterministic retry policy

2) **Agentic**
- Tool calls + planner loop
- Hard caps on tool calls
- Schema validation + repair loop

Evaluation harness compares:
- Schema validity rate
- Field accuracy (or graded correctness)
- Latency / cost proxies
- Failure mode taxonomy

---

## Implemented baseline

Completed in repo:
1) Scaffolded directory tree for `shared/`, `use_cases/customer_doc_triage/experiments/agents_vs_workflows/`, and `experiments/tabular_baselines`.
2) Added root `pyproject.toml` with ruff/pytest config.
3) Added installable `src/` packages for all baseline projects.
4) Added `scripts/setup_repo.sh` for reproducible bootstrap.
5) Added minimal READMEs with CODED/DESIGN markers.
6) Added smoke tests and validated baseline with `pytest`.

---
