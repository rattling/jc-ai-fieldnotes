# Repository Field Notes

A plain-language guide to how this repo explores practical AI system design.

## In one sentence
This repo is about **demystifying agent frameworks**: when they are meaningfully different from a normal workflow with an LLM step, and what guardrails are required to use that extra autonomy safely.

## Why this exists
This repository is where we test ideas about applied AI in realistic workflows.
The goal is not just model quality, but decision quality under constraints: safety, policy, reliability, and operational clarity.

Think of this as a running notebook for **how we reason**, not only what we build.

## Why this is significant
Many teams ask: “Do we really need an agent framework, or is a good workflow with an LLM enough?”

Our first use case is intentionally built to answer that question in a way that is:
- **practical** (real workflow framing, not toy prompts),
- **fair** (same data and output contract across A/B),
- **governable** (explicit safety and policy boundaries),
- **explainable** (clear logs, paths, and evaluation artifacts).

## Who this is for
- **New DS/ML practitioners:** a quick path to what matters and why.
- **Experienced DS/ML/AI engineers:** architecture and evaluation patterns you can reuse.
- **Business and product stakeholders:** clear framing of trade-offs and outcomes without implementation overload.

## How to read this repo
1. Start with a use case to understand the business problem.
2. Review the experiment comparison (what variable changed, what stayed constant).
3. Look at results and field notes for lessons learned.
4. Dive into technical docs or notebook only if you need detail.

## Current use case: customer document triage
**Question:** when routing customer documents, when is a fixed workflow enough, and when is agent-style reasoning worth the extra complexity?

### Experiment: agents vs workflows
We compare two approaches on the same synthetic dataset and output schema:
- **Workflow-constrained mode:** predictable, step-by-step path with bounded repair.
- **Agentic mode:** can choose tool usage/order at runtime under strict guardrails.

### Plain-English difference: workflow + LLM vs agentic system
- **Workflow + LLM:** “Follow this checklist, call the model at step X, then continue.”
- **Agentic system:** “Given these tools/data, decide what to do next and in what order, within hard limits.”

Technical translation:
- Workflow usually has a fixed execution graph.
- Agentic execution can update/branch its effective graph during runtime.

This autonomy is the benefit **and** the risk. That is why guardrails are first-class.

### Why guardrails are non-negotiable
More autonomy means more control requirements. In this repo, guardrails include:
- tool allowlists,
- tool-call budgets,
- timeout budgets,
- shared schema + policy validation,
- fail-closed behavior when checks fail.

In short: autonomy without controls is a demo; autonomy with controls is a system.

## Current scope
- **Use case count:** 1 (`customer_doc_triage`)
- **Experiment count in this use case:** 1 (`agents_vs_workflows`)
- **Intent:** establish a strong baseline pattern before adding more experiments.

## What we are seeing in practice (current run)
On the current 200-document synthetic corpus, the “agent vs workflow” difference is visible in behavior, not only in naming.

### 1) The agent actually changes its execution path by situation
We currently see three recurring runtime subgraphs:
- **General triage path (107 cases):** `detect_doc_type -> extract_metadata -> check_completeness`
   - Mostly `billing_dispute`, `feature_request`, `security_questionnaire`
- **Incident path (52 cases):** `detect_doc_type -> extract_metadata -> check_completeness -> risk_scan`
   - Primarily `incident_report`
- **Privileged-access/policy path (41 cases):** `detect_doc_type -> lookup_policy_context -> risk_scan -> check_completeness`
   - Primarily `access_request`

That is the practical meaning of “agentic”: sequence selection changes with case context.

### 2) Guardrails make the autonomy operationally usable
The dynamic path selection happens inside hard limits:
- allowed tool list,
- tool-call budget,
- timeout budget,
- shared schema/policy validation,
- fail-closed decision when checks fail.

This keeps autonomy bounded and auditable.

### 3) Quality and behavior both move
Current summary metrics:
- Workflow doc type / queue accuracy: **0.915 / 0.915**
- Agent doc type / queue accuracy: **1.000 / 1.000**
- Missing-field recall: **0.965** (workflow) vs **1.000** (agent)
- Escalation recall: **1.000** for both
- Distinct step patterns: **1** (workflow) vs **3** (agent)

So the significance is two-dimensional:
- **Outcome quality** can improve,
- and **reasoning structure** changes in a measurable, explainable way.

## Key takeaways
- **Behavioral difference is concrete:** workflow stays on one path; agent selects among three observed subgraphs based on case context.
- **Control model is explicit:** dynamic behavior is bounded by allowlists, budgets, timeout, and fail-closed validation.
- **Current outcome signal is positive for agent mode:** higher routing/classification quality on this synthetic corpus, with higher tool usage.
- **Execution is reproducible:** notebook + eval flow now run reliably across typical local working-directory setups.

## Quick links
### Start here (non-technical to technical)
- Use-case overview: [customer_doc_triage](../use_cases/customer_doc_triage/README.md)
- Experiment overview: [agents_vs_workflows README](../use_cases/customer_doc_triage/experiments/agents_vs_workflows/README.md)
- Detailed experiment field notes: [agents_vs_workflows FIELDNOTES](../use_cases/customer_doc_triage/experiments/agents_vs_workflows/docs/FIELDNOTES.md)

### Process and architecture details
- Domain and context: [01_domain_and_use_case.md](../use_cases/customer_doc_triage/experiments/agents_vs_workflows/docs/01_domain_and_use_case.md)
- As-is process: [02_as_is_process.md](../use_cases/customer_doc_triage/experiments/agents_vs_workflows/docs/02_as_is_process.md)
- Target designs + ADR: [04_target_designs_and_adr.md](../use_cases/customer_doc_triage/experiments/agents_vs_workflows/docs/04_target_designs_and_adr.md)
- Architecture deep dive: [06_architecture.md](../use_cases/customer_doc_triage/experiments/agents_vs_workflows/docs/06_architecture.md)

### Hands-on
- Notebook walkthrough: [ab_comparison_walkthrough.ipynb](../use_cases/customer_doc_triage/experiments/agents_vs_workflows/notebooks/ab_comparison_walkthrough.ipynb)
- Latest evaluation summary: [ab_eval_summary.md](../use_cases/customer_doc_triage/experiments/agents_vs_workflows/eval_outputs/ab_eval_summary.md)

## How we’ll keep this updated
As each experiment matures, we update this page with:
- the core question,
- what changed,
- what stayed fixed,
- and what we learned that is broadly reusable.

That keeps the repo readable for newcomers while preserving technical depth for deeper follow-up.
