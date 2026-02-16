# Domain, Company, and Use Case

## Domain
Customer support operations in a B2B SaaS context, focused on inbound document triage.

The team receives varied customer documents:
- incident reports
- access requests
- security/compliance questionnaires
- billing and contract artifacts
- product bug evidence (screenshots/log extracts)

These documents arrive through multiple channels (ticket attachments, email uploads, portal forms) and must be triaged before downstream handling.

## Company Context (Synthetic)
**Company:** Northstar Cloud (synthetic)

**Product:** Multi-tenant workflow automation platform used by enterprise operations teams.

**Support model:** Tiered support with a shared intake queue and specialist routing.

**Operational constraints:**
- strict SLA windows by customer tier
- compliance obligations for handling sensitive data
- periodic load spikes after major product releases

## Specific Use Case
Use LLM-enabled systems to improve triage quality and speed for inbound customer documents.

Triage outcome should include:
- document type classification
- priority/severity estimate
- owning team recommendation
- required follow-up fields (missing metadata)
- confidence and escalation flags

## Current Baseline (No LLM)
Today, triage is mostly manual and rule-driven:
- support coordinators read and tag documents
- static keyword rules assist routing
- predefined forms enforce partial structure
- escalations depend heavily on analyst judgement

This is reliable for known patterns but slow and brittle for novel or mixed-content documents.

## Scope for This Experiment
We compare two LLM-enabled approaches for the same triage goal:
- **Design A (Workflow-constrained):** LLM has bounded responsibility inside a deterministic pipeline
- **Design B (Agentic):** LLM can choose tools and sequence actions under guardrails

Both designs operate on the same synthetic dataset and are evaluated with shared metrics to isolate architectural effects.
