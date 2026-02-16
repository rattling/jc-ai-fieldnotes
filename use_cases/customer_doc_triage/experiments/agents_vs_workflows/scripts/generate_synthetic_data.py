#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import random
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

try:
    from customer_doc_triage.triage.engine import infer_priority
    from customer_doc_triage.triage.policies import find_required_missing_fields, should_escalate
except ModuleNotFoundError:
    repo_root = Path(__file__).resolve().parents[5]
    core_src = repo_root / "use_cases" / "customer_doc_triage" / "src"
    if str(core_src) not in sys.path:
        sys.path.insert(0, str(core_src))
    from customer_doc_triage.triage.engine import infer_priority
    from customer_doc_triage.triage.policies import find_required_missing_fields, should_escalate

DOC_TYPES = [
    "incident_report",
    "access_request",
    "security_questionnaire",
    "billing_dispute",
    "feature_request",
]

DOC_TYPE_WEIGHTS = [0.28, 0.20, 0.18, 0.17, 0.17]
CHANNELS = ["email", "portal", "attachment", "api"]
REGIONS = ["NA", "EU", "APAC", "LATAM"]
TIERS = ["enterprise", "growth", "standard"]

INCIDENT_SERVICES = ["api-gateway", "auth-service", "billing-service", "data-export"]
ACCESS_ROLES = ["admin", "billing-admin", "security-auditor", "support-analyst"]
SECURITY_FRAMEWORKS = ["SOC2", "ISO27001", "HIPAA", "GDPR"]
BILLING_ISSUES = ["duplicate charge", "invoice mismatch", "unexpected overage", "tax issue"]
FEATURE_AREAS = ["workflow builder", "audit logs", "SAML setup", "reporting dashboard"]

QUEUES = {
    "incident_report": "support_incident",
    "access_request": "security_access",
    "security_questionnaire": "compliance_ops",
    "billing_dispute": "billing_ops",
    "feature_request": "product_feedback",
}


@dataclass
class GeneratedCase:
    sample: dict[str, Any]
    gold: dict[str, Any]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate synthetic triage dataset.")
    parser.add_argument("--count", type=int, default=200, help="Number of documents to generate.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for deterministic generation.")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data",
        help="Output data directory containing samples.jsonl and gold.jsonl.",
    )
    parser.add_argument(
        "--edge-rate",
        type=float,
        default=0.30,
        help="Fraction of cases to inject with edge-case behavior.",
    )
    return parser.parse_args()


def weighted_choice(randomizer: random.Random) -> str:
    return randomizer.choices(DOC_TYPES, weights=DOC_TYPE_WEIGHTS, k=1)[0]


def make_doc_type_hint(doc_type: str, randomizer: random.Random, edge_case: bool) -> str:
    if edge_case and randomizer.random() < 0.35:
        alternatives = [candidate for candidate in DOC_TYPES if candidate != doc_type]
        return randomizer.choice(alternatives).replace("_", " ")
    return doc_type.replace("_", " ")


def maybe_missing_tier(randomizer: random.Random, edge_case: bool) -> str | None:
    if edge_case and randomizer.random() < 0.35:
        return None
    if randomizer.random() < 0.08:
        return None
    return randomizer.choice(TIERS)


def make_timestamp(randomizer: random.Random) -> str:
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    offset_days = randomizer.randint(0, 45)
    offset_minutes = randomizer.randint(0, 24 * 60 - 1)
    ts = start + timedelta(days=offset_days, minutes=offset_minutes)
    return ts.isoformat().replace("+00:00", "Z")


def build_incident(randomizer: random.Random, edge_case: bool) -> tuple[str, dict[str, Any]]:
    service = randomizer.choice(INCIDENT_SERVICES)
    region = randomizer.choice(REGIONS)
    latency = randomizer.randint(120, 900)
    content = (
        f"Production incident: {service} latency spiked to {latency}ms in {region}. "
        "Customer reports intermittent failures during peak traffic."
    )
    metadata: dict[str, Any] = {
        "service": service,
        "region": region,
        "has_logs": randomizer.random() > 0.15,
        "request_id_examples": "req-1001,req-1002",
    }

    if edge_case and randomizer.random() < 0.45:
        metadata.pop("request_id_examples", None)
        content += " Unable to attach request IDs yet."

    return content, metadata


def build_access_request(randomizer: random.Random, edge_case: bool) -> tuple[str, dict[str, Any]]:
    role = randomizer.choice(ACCESS_ROLES)
    window = randomizer.choice(["overnight migration", "month-end close", "audit prep"])
    content = (
        f"Requesting temporary {role} permissions for external contractor during {window}."
    )
    metadata = {
        "requested_role": role,
        "temporary_access": True,
        "justification": "operational requirement",
        "approval_reference": f"APR-{randomizer.randint(1000, 9999)}",
    }

    if edge_case and randomizer.random() < 0.50:
        metadata.pop("approval_reference", None)
        content += " Approver details not included in submission."

    return content, metadata


def build_security_questionnaire(randomizer: random.Random, edge_case: bool) -> tuple[str, dict[str, Any]]:
    framework = randomizer.choice(SECURITY_FRAMEWORKS)
    due_days = randomizer.randint(2, 14)
    required_due_date = (datetime(2026, 3, 1, tzinfo=timezone.utc) + timedelta(days=due_days)).date().isoformat()
    content = (
        f"Customer sent security questionnaire for {framework} review. "
        "Needs completion before procurement deadline."
    )
    metadata = {
        "framework": framework,
        "question_count": randomizer.randint(20, 180),
        "required_due_date": required_due_date,
        "deadline_days": due_days,
    }

    if edge_case and randomizer.random() < 0.35:
        metadata.pop("required_due_date", None)
        content += " Submission deadline not clearly stated."

    return content, metadata


def build_billing_dispute(randomizer: random.Random, edge_case: bool) -> tuple[str, dict[str, Any]]:
    issue = randomizer.choice(BILLING_ISSUES)
    amount = randomizer.randint(400, 12000)
    content = (
        f"Customer disputes invoice due to {issue}. "
        f"Disputed amount is approximately ${amount}."
    )
    metadata = {
        "issue_type": issue,
        "disputed_amount": amount,
        "invoice_id": f"INV-{randomizer.randint(10000, 99999)}",
    }

    if edge_case and randomizer.random() < 0.40:
        metadata.pop("invoice_id", None)
        content += " Invoice identifier not provided in the message."

    return content, metadata


def build_feature_request(randomizer: random.Random, edge_case: bool) -> tuple[str, dict[str, Any]]:
    area = randomizer.choice(FEATURE_AREAS)
    content = (
        f"Feature request: improve {area} for enterprise rollout. "
        "Current workflow requires too many manual steps."
    )
    metadata = {
        "product_area": area,
        "customer_impact": randomizer.choice(["low", "medium", "high"]),
        "business_justification": "Customer reports measurable efficiency gains if implemented.",
    }

    if edge_case and randomizer.random() < 0.30:
        metadata.pop("business_justification", None)
        content += " Business impact details are currently limited."

    return content, metadata


def build_case_fields(doc_type: str, randomizer: random.Random, edge_case: bool) -> tuple[str, dict[str, Any]]:
    if doc_type == "incident_report":
        return build_incident(randomizer, edge_case)
    if doc_type == "access_request":
        return build_access_request(randomizer, edge_case)
    if doc_type == "security_questionnaire":
        return build_security_questionnaire(randomizer, edge_case)
    if doc_type == "billing_dispute":
        return build_billing_dispute(randomizer, edge_case)
    return build_feature_request(randomizer, edge_case)


def generate_case(index: int, randomizer: random.Random, edge_rate: float) -> GeneratedCase:
    doc_type = weighted_choice(randomizer)
    edge_case = randomizer.random() < edge_rate

    customer_id = f"CUST-{randomizer.randint(1000, 9999)}"
    tier = maybe_missing_tier(randomizer, edge_case)
    region = randomizer.choice(REGIONS)
    channel = randomizer.choice(CHANNELS)

    content, metadata = build_case_fields(doc_type, randomizer, edge_case)

    if edge_case and randomizer.random() < 0.2:
        content += " Also seeing invoice anomalies this week."

    missing_fields = find_required_missing_fields(doc_type=doc_type, metadata=metadata)
    priority, severity = infer_priority(doc_type, tier, missing_fields)
    queue = QUEUES[doc_type]
    escalate, escalation_reason = should_escalate(
        doc_type=doc_type,
        customer_tier=tier,
        missing_fields=missing_fields,
        priority=priority,
    )

    doc_id = f"DOC-{index:04d}"
    sample = {
        "doc_id": doc_id,
        "channel": channel,
        "customer_id": customer_id,
        "customer_tier": tier,
        "region": region,
        "submitted_at": make_timestamp(randomizer),
        "doc_type_hint": make_doc_type_hint(doc_type, randomizer, edge_case),
        "content": content,
        "metadata": metadata,
    }

    gold = {
        "doc_id": doc_id,
        "true_doc_type": doc_type,
        "priority": priority,
        "severity_score": severity,
        "recommended_queue": queue,
        "required_missing_fields": missing_fields,
        "escalate": escalate,
        "escalation_reason": escalation_reason,
    }

    return GeneratedCase(sample=sample, gold=gold)


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> None:
    args = parse_args()
    randomizer = random.Random(args.seed)

    args.data_dir.mkdir(parents=True, exist_ok=True)
    sample_rows: list[dict[str, Any]] = []
    gold_rows: list[dict[str, Any]] = []

    for index in range(1, args.count + 1):
        case = generate_case(index=index, randomizer=randomizer, edge_rate=args.edge_rate)
        sample_rows.append(case.sample)
        gold_rows.append(case.gold)

    samples_path = args.data_dir / "samples.jsonl"
    gold_path = args.data_dir / "gold.jsonl"

    write_jsonl(samples_path, sample_rows)
    write_jsonl(gold_path, gold_rows)

    print(f"Generated {len(sample_rows)} samples: {samples_path}")
    print(f"Generated {len(gold_rows)} gold labels: {gold_path}")


if __name__ == "__main__":
    main()
