# Problem Statement

## Why Current Triage Underperforms

### 1) Throughput bottlenecks
Manual first-pass reading does not scale with bursty document volume.

### 2) Decision variance
Different coordinators make different routing and severity calls on similar inputs.

### 3) Rule brittleness
Static rules miss semantic intent and fail on phrasing drift, mixed documents, and ambiguous language.

### 4) Rework overhead
Downstream queues frequently bounce tickets back due to incomplete metadata or poor categorization.

### 5) Weak observability
Current process lacks structured confidence signals and explicit uncertainty handling.

## Consequences
- SLA misses increase during demand spikes.
- Specialist teams spend time correcting intake errors.
- Customer experience degrades due to extra back-and-forth.
- Triage quality depends too heavily on individual operator skill.

## Outcome Targets for Replacement
- faster first-pass triage latency
- improved routing precision and severity calibration
- fewer rework loops
- explicit confidence-based escalation behavior
- auditable triage rationale and decision trace
