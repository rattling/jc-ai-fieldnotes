# Architecture — Agents vs Workflows

## Scope
This architecture covers the triage stage only:
- ingest customer document
- produce structured triage decision
- route or escalate

Downstream specialist resolution is out of scope.

## Key architectural decisions

### AD-01: Shared core, swappable orchestration modes
- **Decision:** Keep shared ingestion/schema/policy/eval components, swap only orchestration mode (A vs B).
- **Why:** Enables fair comparison and isolates the control-flow variable.

### AD-02: Ports-and-adapters at IO boundaries
- **Decision:** External interactions (LLM, retrieval, policy sources, persistence) go through adapters.
- **Why:** Keeps domain/application logic testable and provider-agnostic.

### AD-03: Schema-first contract at triage output boundary
- **Decision:** Both A and B must emit the same triage schema and pass the same validators.
- **Why:** Supports apples-to-apples evaluation and safer integration.

### AD-04: Guardrailed agent loop for Option B
- **Decision:** B uses tool allowlist, max tool calls, timeout budget, and mandatory final validation.
- **Why:** Balances adaptivity with predictable operational risk.

### AD-05: Deterministic evaluation harness
- **Decision:** Evaluate A and B on the same synthetic snapshot and shared metrics.
- **Why:** Prevents data drift from distorting architecture comparison.

## Technology choices
- Python 3.11 runtime
- `pydantic` for boundary schemas
- `pytest` + lightweight fixtures for component/integration tests
- JSONL corpus (`samples.jsonl`, `gold.jsonl`) for reproducible experiment inputs

No heavy orchestration framework is required initially; simple runners are preferred for clarity.

## Component diagram
```mermaid
flowchart LR
    A[Input Corpus JSONL] --> B[Ingestion and Parsing Adapter]
    B --> C[Application Orchestrator]
    C --> D[Shared Domain Policies]
    C --> E[Triage Schema Validator]

    C --> F[Option A Runner Fixed Flow]
    C --> G[Option B Runner Agent Loop]

    F --> H[LLM Adapter]
    G --> H
    G --> I[Tool Adapters]

    F --> J[Triage Decision]
    G --> J
    J --> E
    E --> K[Routing and Escalation Output]
    K --> L[Evaluation Harness]
    A --> L
```

## Sequence diagram — Option A (fixed flow)
```mermaid
sequenceDiagram
    participant R as Runner A
    participant P as Parser
    participant M as LLM Adapter
    participant V as Validator
    participant O as Output

    R->>P: parse document
    P-->>R: normalized payload
    R->>M: bounded triage prompt
    M-->>R: structured candidate
    R->>V: validate schema and policy
    alt valid
        V-->>R: pass
        R->>O: emit triage output
    else invalid
        V-->>R: fail
        R->>M: bounded repair retry
        M-->>R: revised candidate
        R->>V: re-validate
        V-->>R: pass or fail
        R->>O: route or escalate
    end
```

## Sequence diagram — Option B (dynamic flow)
```mermaid
sequenceDiagram
    participant R as Runner B
    participant P as Parser
    participant A as Agent Planner
    participant T as Tool Adapter
    participant V as Validator
    participant O as Output

    R->>P: parse document
    P-->>R: normalized payload
    R->>A: start plan with context
    loop until stop criteria or budget reached
        A->>T: invoke selected tool
        T-->>A: tool result
        A->>A: update working context
    end
    A-->>R: triage candidate
    R->>V: validate schema and policy
    alt valid
        V-->>R: pass
        R->>O: emit triage output
    else invalid
        V-->>R: fail
        R->>O: escalate
    end
```

## State diagram — Triage case lifecycle
```mermaid
stateDiagram-v2
    [*] --> Received
    Received --> Normalized
    Normalized --> InTriage
    InTriage --> AwaitingValidation
    AwaitingValidation --> Routed: validation pass
    AwaitingValidation --> Escalated: validation fail
    Routed --> [*]
    Escalated --> [*]
```

## Build-time invariants
1. Same input corpus for A and B in each evaluation run.
2. Same output schema and validators for A and B.
3. No adapter dependency leakage into domain policy logic.
4. All triage outcomes include trace metadata for debugging.
5. Option B cannot bypass final schema/policy validation.

## Risks to track
- Option B latency/cost drift under tool loops.
- Option A underperformance on ambiguous, mixed-signal cases.
- Hidden coupling between adapters and orchestration logic.

## What else to document as build progresses
- runtime config model (timeouts, budgets, retry caps)
- observability model (event schema, correlation ids)
- test strategy map (unit, contract, integration, replay)
- failure taxonomy with mitigation playbooks
