# A/B Eval Summary

## Overall

| Mode | DocType Acc | Queue Acc | Escalation P | Escalation R | Missing Recall | Avg Elapsed ms | Avg Tool Calls | Step Patterns |
|------|-------------|-----------|--------------|--------------|----------------|----------------|----------------|---------------|
| workflow | 0.925 | 0.925 | 0.500 | 1.000 | 0.970 | 1.0 | 0.00 | 1 |
| agent | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.0 | 3.43 | 3 |

## Slices

### doc_type:access_request

| Mode | Count | DocType Acc | Queue Acc |
|------|-------|-------------|-----------|
| workflow | 33 | 0.909 | 0.909 |
| agent | 33 | 1.000 | 1.000 |

### doc_type:billing_dispute

| Mode | Count | DocType Acc | Queue Acc |
|------|-------|-------------|-----------|
| workflow | 38 | 0.974 | 0.974 |
| agent | 38 | 1.000 | 1.000 |

### doc_type:feature_request

| Mode | Count | DocType Acc | Queue Acc |
|------|-------|-------------|-----------|
| workflow | 43 | 0.907 | 0.907 |
| agent | 43 | 1.000 | 1.000 |

### doc_type:incident_report

| Mode | Count | DocType Acc | Queue Acc |
|------|-------|-------------|-----------|
| workflow | 53 | 0.887 | 0.887 |
| agent | 53 | 1.000 | 1.000 |

### doc_type:security_questionnaire

| Mode | Count | DocType Acc | Queue Acc |
|------|-------|-------------|-----------|
| workflow | 33 | 0.970 | 0.970 |
| agent | 33 | 1.000 | 1.000 |

### slice:edge_case

| Mode | Count | DocType Acc | Queue Acc |
|------|-------|-------------|-----------|
| workflow | 30 | 0.800 | 0.800 |
| agent | 30 | 1.000 | 1.000 |

### slice:non_edge_case

| Mode | Count | DocType Acc | Queue Acc |
|------|-------|-------------|-----------|
| workflow | 170 | 0.947 | 0.947 |
| agent | 170 | 1.000 | 1.000 |
