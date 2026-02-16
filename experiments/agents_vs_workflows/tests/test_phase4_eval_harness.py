from __future__ import annotations

import json
from pathlib import Path

from agents_vs_workflows.eval.harness import run_eval


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row) + "\n")


def test_eval_harness_generates_summary_and_artifacts(tmp_path: Path):
    samples = [
        {
            "doc_id": "DOC-EVAL-1",
            "channel": "email",
            "customer_id": "CUST-1",
            "customer_tier": "enterprise",
            "region": "EU",
            "submitted_at": "2026-02-16T12:00:00Z",
            "doc_type_hint": "access request",
            "content": "Need temporary privileged admin access for contractor.",
            "metadata": {
                "requested_role": "admin",
                "justification": "migration",
                "approval_reference": "CHG-1",
            },
        },
        {
            "doc_id": "DOC-EVAL-2",
            "channel": "portal",
            "customer_id": "CUST-2",
            "customer_tier": "growth",
            "region": "NA",
            "submitted_at": "2026-02-16T13:00:00Z",
            "doc_type_hint": "billing dispute",
            "content": "Customer disputes invoice due to duplicate charge.",
            "metadata": {
                "issue_type": "duplicate charge",
                "invoice_id": "INV-1",
            },
        },
    ]

    gold = [
        {
            "doc_id": "DOC-EVAL-1",
            "true_doc_type": "access_request",
            "priority": "P1",
            "severity_score": 5,
            "recommended_queue": "security_access",
            "required_missing_fields": [],
            "escalate": True,
            "escalation_reason": "Privileged access request for regulated/high-tier account",
        },
        {
            "doc_id": "DOC-EVAL-2",
            "true_doc_type": "billing_dispute",
            "priority": "P2",
            "severity_score": 3,
            "recommended_queue": "billing_ops",
            "required_missing_fields": [],
            "escalate": False,
            "escalation_reason": None,
        },
    ]

    samples_path = tmp_path / "samples.jsonl"
    gold_path = tmp_path / "gold.jsonl"
    output_dir = tmp_path / "eval_outputs"

    _write_jsonl(samples_path, samples)
    _write_jsonl(gold_path, gold)

    result = run_eval(samples_path=samples_path, gold_path=gold_path, output_dir=output_dir)
    summary = result["summary"]

    assert summary["corpus_size"] == 2
    assert "workflow" in summary["modes"]
    assert "agent" in summary["modes"]

    assert (output_dir / "ab_eval_summary.json").exists()
    assert (output_dir / "ab_eval_summary.md").exists()
    assert (output_dir / "per_case_predictions.csv").exists()