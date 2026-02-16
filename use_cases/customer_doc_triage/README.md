# customer_doc_triage

Core use-case boundary for customer document triage.

## Purpose
Hold shared scenario assets for this domain while enabling multiple focused experiments.

## Boundary
- Shared business context, schemas, policy assumptions, and evaluation semantics live at use-case level.
- Individual experiments change one primary variable at a time (orchestration mode, thresholds, retrieval strategy, etc.).

## Current experiments
- `experiments/agents_vs_workflows`

## Expansion model
One use case can host multiple experiments and findings:
- `experiments/<experiment_name>/...`
- docs and artifacts remain scoped to each experiment
- findings are comparable because they share the same use-case framing
