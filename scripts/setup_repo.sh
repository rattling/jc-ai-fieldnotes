#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

DO_SCAFFOLD=0
if [[ "${1:-}" == "--scaffold" ]]; then
  DO_SCAFFOLD=1
fi

log() {
  echo "[setup_repo] $*"
}

require_path() {
  local path="$1"
  if [[ ! -e "$path" ]]; then
    log "missing required path: $path"
    log "for an existing clone, ensure you are at repo root and all files are present"
    log "or run with --scaffold to create baseline paths/files"
    exit 1
  fi
}

scaffold_repo() {
  log "scaffolding baseline repository layout (opt-in)"
  mkdir -p scripts docs shared/src/shared shared/tests
  mkdir -p use_cases/customer_doc_triage/src/customer_doc_triage
  mkdir -p use_cases/customer_doc_triage/experiments/agents_vs_workflows/data
  mkdir -p use_cases/customer_doc_triage/experiments/agents_vs_workflows/tests
  mkdir -p use_cases/customer_doc_triage/experiments/agents_vs_workflows/src/agents_vs_workflows

  if [[ ! -f .python-version ]]; then
    printf "3.11\n" > .python-version
    log "created .python-version"
  fi
}

if [[ "$DO_SCAFFOLD" -eq 1 ]]; then
  scaffold_repo
else
  log "running install-first setup (no scaffolding). use --scaffold only for recovery/bootstrap"
  require_path "pyproject.toml"
  require_path "shared/pyproject.toml"
  require_path "use_cases/customer_doc_triage/pyproject.toml"
  require_path "use_cases/customer_doc_triage/experiments/agents_vs_workflows/pyproject.toml"
fi

if ! command -v uv >/dev/null 2>&1; then
  log "uv not found; install it first: https://docs.astral.sh/uv/"
  exit 1
fi

log "creating/updating root virtual environment"
uv venv -p 3.11

log "installing core dev tooling"
uv pip install --python .venv/bin/python ruff pytest hatchling

log "installing local packages in editable mode"
uv pip install --python .venv/bin/python \
  -e shared \
  -e use_cases/customer_doc_triage \
  -e use_cases/customer_doc_triage/experiments/agents_vs_workflows

log "setup complete"
log "activate with: source .venv/bin/activate"
