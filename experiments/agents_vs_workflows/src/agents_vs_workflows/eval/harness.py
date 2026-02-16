from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from agents_vs_workflows.agent.pipeline import run_agentic
from agents_vs_workflows.eval.metrics import score
from agents_vs_workflows.workflow.pipeline import run_workflow


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped:
                rows.append(json.loads(stripped))
    return rows


def _gold_index(gold_rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {row["doc_id"]: row for row in gold_rows}


def _decision_to_prediction(mode: str, decision: Any) -> dict[str, Any]:
    payload = decision.model_dump()
    payload["mode"] = mode
    return payload


def _run_mode(mode: str, samples: list[dict[str, Any]]) -> list[dict[str, Any]]:
    predictions: list[dict[str, Any]] = []

    for sample in samples:
        if mode == "workflow":
            decision = run_workflow(sample, max_retries=1)
        elif mode == "agent":
            decision = run_agentic(sample, max_tool_calls=6, timeout_ms=2_000)
        else:
            raise ValueError(f"Unsupported mode: {mode}")

        predictions.append(_decision_to_prediction(mode, decision))

    return predictions


def _write_predictions_csv(path: Path, predictions: list[dict[str, Any]]) -> None:
    fieldnames = [
        "mode",
        "doc_id",
        "doc_type",
        "priority",
        "recommended_queue",
        "escalate",
        "escalation_reason",
        "confidence",
        "required_missing_fields",
        "tool_calls",
        "elapsed_ms",
    ]

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()

        for prediction in predictions:
            trace = prediction.get("decision_trace", {})
            writer.writerow(
                {
                    "mode": prediction.get("mode"),
                    "doc_id": prediction.get("doc_id"),
                    "doc_type": prediction.get("doc_type"),
                    "priority": prediction.get("priority"),
                    "recommended_queue": prediction.get("recommended_queue"),
                    "escalate": prediction.get("escalate"),
                    "escalation_reason": prediction.get("escalation_reason"),
                    "confidence": prediction.get("confidence"),
                    "required_missing_fields": ",".join(
                        prediction.get("required_missing_fields", [])
                    ),
                    "tool_calls": trace.get("tool_calls", 0),
                    "elapsed_ms": trace.get("elapsed_ms", 0),
                }
            )


def _write_markdown_summary(path: Path, summary: dict[str, Any]) -> None:
    lines = ["# A/B Eval Summary", ""]
    lines.append("## Overall")
    lines.append("")
    lines.append("| Mode | DocType Acc | Queue Acc | Escalation P | Escalation R | Missing Recall | Avg Elapsed ms | Avg Tool Calls |")
    lines.append("|------|-------------|-----------|--------------|--------------|----------------|----------------|----------------|")

    for mode in ("workflow", "agent"):
        metrics = summary["modes"][mode]
        lines.append(
            "| "
            f"{mode} | "
            f"{metrics['doc_type_accuracy']:.3f} | "
            f"{metrics['queue_accuracy']:.3f} | "
            f"{metrics['escalation_precision']:.3f} | "
            f"{metrics['escalation_recall']:.3f} | "
            f"{metrics['missing_field_recall']:.3f} | "
            f"{metrics['avg_elapsed_ms']:.1f} | "
            f"{metrics['avg_tool_calls']:.2f} |"
        )

    lines.append("")
    lines.append("## Slices")
    lines.append("")

    slice_labels = sorted(summary["modes"]["workflow"]["slices"].keys())
    for label in slice_labels:
        workflow_slice = summary["modes"]["workflow"]["slices"][label]
        agent_slice = summary["modes"]["agent"]["slices"].get(label, {})
        lines.append(f"### {label}")
        lines.append("")
        lines.append("| Mode | Count | DocType Acc | Queue Acc |")
        lines.append("|------|-------|-------------|-----------|")
        lines.append(
            f"| workflow | {workflow_slice.get('count', 0)} | "
            f"{workflow_slice.get('doc_type_accuracy', 0.0):.3f} | "
            f"{workflow_slice.get('queue_accuracy', 0.0):.3f} |"
        )
        lines.append(
            f"| agent | {agent_slice.get('count', 0)} | "
            f"{agent_slice.get('doc_type_accuracy', 0.0):.3f} | "
            f"{agent_slice.get('queue_accuracy', 0.0):.3f} |"
        )
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def run_eval(
    samples_path: Path,
    gold_path: Path,
    output_dir: Path,
) -> dict[str, Any]:
    samples = _read_jsonl(samples_path)
    gold_rows = _read_jsonl(gold_path)
    gold = _gold_index(gold_rows)

    workflow_predictions = _run_mode("workflow", samples)
    agent_predictions = _run_mode("agent", samples)

    summary = {
        "corpus_size": len(samples),
        "modes": {
            "workflow": score(workflow_predictions, gold),
            "agent": score(agent_predictions, gold),
        },
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    summary_json_path = output_dir / "ab_eval_summary.json"
    summary_md_path = output_dir / "ab_eval_summary.md"
    predictions_csv_path = output_dir / "per_case_predictions.csv"

    summary_json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    _write_markdown_summary(summary_md_path, summary)
    _write_predictions_csv(predictions_csv_path, workflow_predictions + agent_predictions)

    return {
        "summary": summary,
        "summary_json": str(summary_json_path),
        "summary_md": str(summary_md_path),
        "predictions_csv": str(predictions_csv_path),
    }