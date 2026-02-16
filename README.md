# jc-ai-fieldnotes

Reproducible monorepo bootstrap for AI fieldnotes experiments.

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