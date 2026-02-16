# Implementation Plan — Agents vs Workflows

Status legend:
- `[ ]` not started
- `[-]` in progress
- `[x]` done

## Working style (for this experiment)
- Keep tasks small and stateful.
- Check off items in this doc as work completes.
- Commit at the end of each completed task chunk.
- Keep `A` and `B` comparable by reusing shared components.
- Treat this file as the source of truth for session rehydration.

## Phase 1 — Shared contracts and core plumbing

### 1.1 Triage contracts
- [x] Define input schema (`TriageInput`)
- [x] Define output schema (`TriageDecision`)
- [x] Define trace metadata schema (`DecisionTrace`)
- [x] Add schema validation tests

Exit criteria:
- [x] All schemas load and validate via `pytest`
- [x] Output schema supports both A and B without mode-specific fields

### 1.2 Shared policy and validation
- [x] Implement required-field policy checks
- [x] Implement routing policy mapping
- [x] Implement escalation policy checks
- [x] Add deterministic policy tests

Exit criteria:
- [x] Policy behavior covered for happy-path and edge cases
- [x] No adapter imports in domain/policy modules

## Phase 2 — Option A runner (fixed flow)

### 2.1 Runner implementation
- [ ] Implement parse -> prompt -> validate -> route loop
- [ ] Implement bounded repair retry path
- [ ] Emit structured trace metadata

### 2.2 Tests
- [ ] Unit tests for retry and validation behavior
- [ ] Integration test on small fixture subset

Exit criteria:
- [ ] Option A runs end-to-end on fixture corpus
- [ ] Failure path escalates correctly

## Phase 3 — Option B runner (dynamic flow)

### 3.1 Guardrailed agent loop
- [ ] Implement tool allowlist
- [ ] Implement max tool calls and timeout budget
- [ ] Implement stop criteria and final output assembly
- [ ] Enforce mandatory final schema/policy validation

### 3.2 Tests
- [ ] Unit tests for budget and allowlist enforcement
- [ ] Integration test with at least two distinct case patterns

Exit criteria:
- [ ] Option B shows case-dependent subgraph behavior
- [ ] Guardrail violations always fail closed (escalate)

## Phase 4 — Replay eval harness (A vs B)

### 4.1 Harness and metrics
- [ ] Add runner to replay on `data/samples.jsonl`
- [ ] Join predictions with `data/gold.jsonl`
- [ ] Compute metrics:
  - [ ] doc-type accuracy
  - [ ] queue accuracy
  - [ ] escalation precision/recall
  - [ ] missing-field recall
  - [ ] latency/cost proxies
- [ ] Add slice reporting by doc type and edge-case flag

### 4.2 Reproducibility
- [ ] Save eval output artifacts (json/csv/markdown summary)
- [ ] Add deterministic run command to README

Exit criteria:
- [ ] Same harness executes A and B on identical snapshot
- [ ] Comparison report generated in one command

## Phase 5 — Findings and hardening

### 5.1 Findings
- [ ] Add fieldnote with first A vs B metric readout
- [ ] Record surprising failures and probable causes
- [ ] Capture architecture implications (keep/change)

### 5.2 Hardening
- [ ] Add regression tests for top 3 observed failure modes
- [ ] Refine prompts/policies with minimal complexity increase

Exit criteria:
- [ ] Decision-ready summary for next iteration
- [ ] Candidate tag point for experiment milestone

---

## Session rehydration protocol

Use this at the start of any new work session:

1. Open this plan file and identify the first `[-]` or `[ ]` item.
2. Run quick repo state check:
   - `git status --short`
   - `pytest -q` (or targeted subset)
3. Re-read key docs (fast pass):
   - `docs/06_architecture.md`
   - `docs/FIELDNOTES.md`
   - this file
4. Continue from the current phase item only (avoid parallel drift).

## Commit protocol
- Commit after each coherent completed chunk (usually one checklist group).
- Use commit messages that map to phase/task ids.

Suggested commit format:
- `P1.1: add triage input/output schemas and tests`
- `P2.1: implement option A fixed-flow runner`
- `P4.1: add replay harness and core metrics`

## Session handoff template
Append/update this block at end of session (in commit message or notes):

- **Completed:**
- **In progress:**
- **Next item:**
- **Commands to resume:**
- **Open risks/questions:**

## Scope guardrails
- Do not add framework complexity unless triggered by architecture policy.
- Keep shared schema/policy/eval components identical for A and B.
- Prefer clarity and debuggability over abstraction density.
