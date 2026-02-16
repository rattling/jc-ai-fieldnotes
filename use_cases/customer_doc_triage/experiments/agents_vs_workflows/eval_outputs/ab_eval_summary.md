# A/B Eval Summary

## Overall

| Mode | DocType Acc | Queue Acc | Escalation P | Escalation R | Missing Recall | Avg Elapsed ms | Avg Tool Calls | Step Patterns |
|------|-------------|-----------|--------------|--------------|----------------|----------------|----------------|---------------|
| workflow | 0.915 | 0.915 | 0.212 | 1.000 | 0.965 | 0.0 | 0.00 | 1 |
| agent | 1.000 | 1.000 | 0.258 | 1.000 | 1.000 | 0.0 | 3.46 | 3 |

## Slices

### doc_type:access_request

| Mode | Count | DocType Acc | Queue Acc |
|------|-------|-------------|-----------|
| workflow | 41 | 0.902 | 0.902 |
| agent | 41 | 1.000 | 1.000 |

### doc_type:billing_dispute

| Mode | Count | DocType Acc | Queue Acc |
|------|-------|-------------|-----------|
| workflow | 35 | 0.886 | 0.886 |
| agent | 35 | 1.000 | 1.000 |

### doc_type:feature_request

| Mode | Count | DocType Acc | Queue Acc |
|------|-------|-------------|-----------|
| workflow | 38 | 0.895 | 0.895 |
| agent | 38 | 1.000 | 1.000 |

### doc_type:incident_report

| Mode | Count | DocType Acc | Queue Acc |
|------|-------|-------------|-----------|
| workflow | 52 | 0.962 | 0.962 |
| agent | 52 | 1.000 | 1.000 |

### doc_type:security_questionnaire

| Mode | Count | DocType Acc | Queue Acc |
|------|-------|-------------|-----------|
| workflow | 34 | 0.912 | 0.912 |
| agent | 34 | 1.000 | 1.000 |

### slice:edge_case

| Mode | Count | DocType Acc | Queue Acc |
|------|-------|-------------|-----------|
| workflow | 35 | 0.800 | 0.800 |
| agent | 35 | 1.000 | 1.000 |

### slice:non_edge_case

| Mode | Count | DocType Acc | Queue Acc |
|------|-------|-------------|-----------|
| workflow | 165 | 0.939 | 0.939 |
| agent | 165 | 1.000 | 1.000 |
