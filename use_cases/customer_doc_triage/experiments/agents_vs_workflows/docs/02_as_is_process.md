# As-Is Process and BPMs

This describes how document triage is performed today without LLMs.

## Process Summary
1. Intake receives new document and basic metadata.
2. Coordinator performs initial read and categorization.
3. Rule engine runs keyword and regex checks.
4. Coordinator adjusts priority and routing destination.
5. Ticket is forwarded to specialist queue.
6. Rework loop occurs if metadata is incomplete or routing is incorrect.

## BPM 1: Main Triage Flow
```mermaid
flowchart TD
    A[Document received] --> B[Attach to ticket]
    B --> C[Coordinator reads document]
    C --> D[Apply static rules]
    D --> E{Rule match quality high?}
    E -- Yes --> F[Set category and route]
    E -- No --> G[Manual judgement and route]
    F --> H[Set priority and SLA]
    G --> H
    H --> I[Send to specialist queue]
    I --> J{Queue accepts?}
    J -- Yes --> K[Work starts]
    J -- No --> L[Return for re-triage]
    L --> C
```

## BPM 2: Exception/Rework Path
```mermaid
flowchart TD
    A[Specialist reviews intake] --> B{Metadata complete?}
    B -- No --> C[Request missing fields]
    C --> D[Customer follow-up delay]
    D --> E[Coordinator updates ticket]
    E --> F[Re-route ticket]
    B -- Yes --> G{Correct destination team?}
    G -- No --> F
    G -- Yes --> H[Proceed with resolution]
```

## Observed Friction Points
- handoff delays between intake and specialists
- inconsistent triage decisions across analysts
- false positives from rigid keyword rules
- repeat rework caused by missing context fields
