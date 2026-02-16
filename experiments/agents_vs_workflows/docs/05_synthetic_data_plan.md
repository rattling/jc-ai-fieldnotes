# Synthetic Data Plan

## Objective
Create a realistic synthetic corpus for customer-document triage so both Design A and Design B are evaluated on the same inputs.

The corpus should support:
- document type classification
- priority and severity estimation
- routing recommendation
- metadata completeness checks
- escalation decisioning under policy constraints

## Dataset Artifacts
- `data/samples.jsonl`: input documents (what the system sees)
- `data/gold.jsonl`: expected triage outputs for evaluation

Both files are aligned by `doc_id`.

## Input Schema (`samples.jsonl`)
Each line is one JSON object:
- `doc_id`: unique id (e.g., `DOC-0001`)
- `channel`: `email` | `portal` | `attachment` | `api`
- `customer_id`: synthetic customer id
- `customer_tier`: `enterprise` | `growth` | `standard` (may be missing)
- `region`: `NA` | `EU` | `APAC` | `LATAM`
- `submitted_at`: ISO8601 timestamp
- `doc_type_hint`: weak/noisy hint of document type
- `content`: free-text document body
- `metadata`: object with optional extracted fields

## Gold Schema (`gold.jsonl`)
Each line is one JSON object:
- `doc_id`
- `true_doc_type`: canonical class
- `priority`: `P1` | `P2` | `P3`
- `severity_score`: integer `1..5`
- `recommended_queue`: destination team
- `required_missing_fields`: list of required but absent fields
- `escalate`: boolean
- `escalation_reason`: nullable string

## Canonical Document Classes
- `incident_report`
- `access_request`
- `security_questionnaire`
- `billing_dispute`
- `feature_request`

## Target Distribution (default 200 docs)
- incident_report: 28%
- access_request: 20%
- security_questionnaire: 18%
- billing_dispute: 17%
- feature_request: 17%

## Difficulty and Edge Cases
The generator should include controlled edge cases:
- missing critical metadata (e.g., customer tier, request ids)
- mixed signals (incident language + billing language in same doc)
- policy-sensitive requests (regulated customer + privileged access)
- low-information submissions

Default target for edge-case share: ~30% of corpus.

## Evaluation Notes
- Compare A and B on identical corpus snapshot.
- Keep schema and policy checks shared.
- Report by overall metrics and by class/edge-case slice.

## Reproducibility
- Deterministic generation via random seed.
- Configurable count via CLI argument.
- Regeneration should overwrite artifacts intentionally.

## Next Build Step
Implement generator script:
- path: `experiments/agents_vs_workflows/scripts/generate_synthetic_data.py`
- command:
  - `python experiments/agents_vs_workflows/scripts/generate_synthetic_data.py --count 200 --seed 42`
