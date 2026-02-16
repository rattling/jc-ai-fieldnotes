#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

log() {
  echo "[setup_repo] $*"
}

create_dir() {
  mkdir -p "$1"
}

write_if_missing() {
  local path="$1"
  local content="$2"
  if [[ ! -f "$path" ]]; then
    printf "%b" "$content" > "$path"
    log "created $path"
  fi
}

ensure_executable() {
  local path="$1"
  chmod +x "$path"
}

log "scaffolding repository layout"

create_dir "scripts"
create_dir "docs"
create_dir "use_cases/customer_doc_triage/src/customer_doc_triage"
create_dir "use_cases/customer_doc_triage/experiments/agents_vs_workflows/src/agents_vs_workflows/agent"
create_dir "use_cases/customer_doc_triage/experiments/agents_vs_workflows/src/agents_vs_workflows/eval"
create_dir "use_cases/customer_doc_triage/experiments/agents_vs_workflows/tests"
create_dir "use_cases/customer_doc_triage/experiments/agents_vs_workflows/data"
create_dir "shared/src/shared"
create_dir "shared/tests"

write_if_missing ".python-version" "3.11\n"

write_if_missing "pyproject.toml" "[tool.ruff]
line-length = 100
target-version = \"py311\"

[tool.pytest.ini_options]
testpaths = [\"shared/tests\", \"use_cases\"]
addopts = \"-q\"
"

write_if_missing "shared/README.md" "# shared\n\nReusable helpers shared across experiments.\n"
write_if_missing "shared/src/shared/__init__.py" ""
write_if_missing "shared/src/shared/logging.py" "def get_logger(name: str):\n    import logging\n\n    return logging.getLogger(name)\n"
write_if_missing "shared/src/shared/eval_utils.py" "def identity(value):\n    return value\n"
write_if_missing "shared/tests/test_shared_smoke.py" "def test_shared_smoke():\n    assert True\n"
write_if_missing "shared/pyproject.toml" "[project]
name = \"shared\"
version = \"0.1.0\"
requires-python = \">=3.11\"
dependencies = []

[build-system]
requires = [\"hatchling\"]
build-backend = \"hatchling.build\"

[tool.hatch.build.targets.wheel]
packages = [\"src/shared\"]
"

write_if_missing "use_cases/customer_doc_triage/src/customer_doc_triage/__init__.py" ""
write_if_missing "use_cases/customer_doc_triage/pyproject.toml" "[project]
name = \"customer-doc-triage\"
version = \"0.1.0\"
requires-python = \">=3.11\"
dependencies = [
  \"pydantic>=2\",
]

[build-system]
requires = [\"hatchling\"]
build-backend = \"hatchling.build\"

[tool.hatch.build.targets.wheel]
packages = [\"src/customer_doc_triage\"]
"

write_if_missing "use_cases/customer_doc_triage/experiments/agents_vs_workflows/README.md" "# agents_vs_workflows\n\nType: CODED\nDepth: MVP\n"
write_if_missing "use_cases/customer_doc_triage/experiments/agents_vs_workflows/src/agents_vs_workflows/__init__.py" ""
write_if_missing "use_cases/customer_doc_triage/experiments/agents_vs_workflows/src/agents_vs_workflows/config.py" "MODEL_NAME = \"gpt-4.1-mini\"\n"
write_if_missing "use_cases/customer_doc_triage/experiments/agents_vs_workflows/src/agents_vs_workflows/workflow/__init__.py" ""
write_if_missing "use_cases/customer_doc_triage/experiments/agents_vs_workflows/src/agents_vs_workflows/workflow/pipeline.py" "def run_workflow() -> dict:\n    return {\"mode\": \"workflow\", \"status\": \"ok\"}\n"
write_if_missing "use_cases/customer_doc_triage/experiments/agents_vs_workflows/src/agents_vs_workflows/workflow/run.py" "from agents_vs_workflows.workflow.pipeline import run_workflow\n\n\ndef main() -> None:\n    print(run_workflow())\n\n\nif __name__ == \"__main__\":\n    main()\n"
write_if_missing "use_cases/customer_doc_triage/experiments/agents_vs_workflows/src/agents_vs_workflows/workflow/schemas.py" "from pydantic import BaseModel\n\n\nclass WorkflowResult(BaseModel):\n    mode: str\n    status: str\n"
write_if_missing "use_cases/customer_doc_triage/experiments/agents_vs_workflows/src/agents_vs_workflows/agent/__init__.py" ""
write_if_missing "use_cases/customer_doc_triage/experiments/agents_vs_workflows/src/agents_vs_workflows/agent/tools.py" "def available_tools() -> list[str]:\n    return [\"search\", \"summarize\"]\n"
write_if_missing "use_cases/customer_doc_triage/experiments/agents_vs_workflows/src/agents_vs_workflows/agent/planner.py" "def plan(task: str) -> list[str]:\n    return [f\"analyze: {task}\", \"respond\"]\n"
write_if_missing "use_cases/customer_doc_triage/experiments/agents_vs_workflows/src/agents_vs_workflows/agent/schemas.py" "from pydantic import BaseModel\n\n\nclass AgentResult(BaseModel):\n    mode: str\n    steps: int\n"
write_if_missing "use_cases/customer_doc_triage/experiments/agents_vs_workflows/src/agents_vs_workflows/agent/run.py" "from agents_vs_workflows.agent.planner import plan\n\n\ndef main() -> None:\n    steps = plan(\"demo\")\n    print({\"mode\": \"agent\", \"steps\": len(steps)})\n\n\nif __name__ == \"__main__\":\n    main()\n"
write_if_missing "use_cases/customer_doc_triage/experiments/agents_vs_workflows/src/agents_vs_workflows/eval/__init__.py" ""
write_if_missing "use_cases/customer_doc_triage/experiments/agents_vs_workflows/src/agents_vs_workflows/eval/metrics.py" "def score() -> float:\n    return 1.0\n"
write_if_missing "use_cases/customer_doc_triage/experiments/agents_vs_workflows/src/agents_vs_workflows/eval/report.py" "from agents_vs_workflows.eval.metrics import score\n\n\ndef main() -> None:\n    print({\"metric\": score()})\n\n\nif __name__ == \"__main__\":\n    main()\n"
write_if_missing "use_cases/customer_doc_triage/experiments/agents_vs_workflows/tests/test_agents_vs_workflows_smoke.py" "from agents_vs_workflows.workflow.pipeline import run_workflow\n\n\ndef test_workflow_smoke():\n    assert run_workflow()[\"status\"] == \"ok\"\n"
write_if_missing "use_cases/customer_doc_triage/experiments/agents_vs_workflows/data/samples.jsonl" ""
write_if_missing "use_cases/customer_doc_triage/experiments/agents_vs_workflows/data/gold.jsonl" ""
write_if_missing "use_cases/customer_doc_triage/experiments/agents_vs_workflows/pyproject.toml" "[project]
name = \"agents-vs-workflows\"
version = \"0.1.0\"
requires-python = \">=3.11\"
dependencies = [
  \"customer-doc-triage>=0.1.0\",
  \"pydantic>=2\",
]

[build-system]
requires = [\"hatchling\"]
build-backend = \"hatchling.build\"

[tool.hatch.build.targets.wheel]
packages = [\"src/agents_vs_workflows\"]
"

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
