# customer_doc_triage

Core use-case boundary for customer document triage.

## Purpose
Hold shared scenario assets for this domain while enabling multiple focused experiments.

## Boundary
- Shared business context, schemas, and policy assumptions live at use-case level in `src/customer_doc_triage`.
- Individual experiments change one primary variable at a time (orchestration mode, thresholds, retrieval strategy, etc.).

## Current experiments
- `experiments/agents_vs_workflows`

## Use-case core package
- `src/customer_doc_triage/triage/schemas.py`
- `src/customer_doc_triage/triage/policies.py`
- `src/customer_doc_triage/triage/validation.py`
- `src/customer_doc_triage/triage/engine.py`

Experiments should consume this package rather than duplicating triage domain code.

## Expansion model
One use case can host multiple experiments and findings:
- `experiments/<experiment_name>/...`
- docs and artifacts remain scoped to each experiment
- findings are comparable because they share the same use-case framing
