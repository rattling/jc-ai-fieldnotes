#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from agents_vs_workflows.agent.pipeline import run_agentic
from agents_vs_workflows.eval.harness import run_eval
from agents_vs_workflows.workflow.pipeline import run_workflow


def _read_jsonl(path: Path, limit: int | None = None) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            raw = line.strip()
            if not raw:
                continue
            rows.append(json.loads(raw))
            if limit is not None and len(rows) >= limit:
                break
    return rows


def _short_result(decision: Any) -> dict[str, Any]:
    dump = decision.model_dump()
    trace = dump.get("decision_trace", {})
    return {
        "doc_id": dump.get("doc_id"),
        "doc_type": dump.get("doc_type"),
        "priority": dump.get("priority"),
        "queue": dump.get("recommended_queue"),
        "escalate": dump.get("escalate"),
        "missing": dump.get("required_missing_fields", []),
        "tool_calls": trace.get("tool_calls", 0),
        "elapsed_ms": trace.get("elapsed_ms", 0),
    }


def _run_per_case(samples: list[dict[str, Any]], mode: str, max_cases_to_print: int = 8) -> None:
    decisions: list[dict[str, Any]] = []

    for sample in samples:
        if mode == "workflow":
            decision = run_workflow(sample, max_retries=1)
        elif mode == "agent":
            decision = run_agentic(sample, max_tool_calls=6, timeout_ms=2_000)
        else:
            raise ValueError(f"Unsupported mode for per-case execution: {mode}")

        decisions.append(_short_result(decision))

    print({"mode": mode, "cases": len(decisions)})
    for row in decisions[:max_cases_to_print]:
        print(row)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run agents_vs_workflows in VS Code-friendly modes (workflow/agent/both/eval)."
    )

    experiment_dir = Path(__file__).resolve().parents[1]
    default_data_dir = experiment_dir / "data"
    default_output_dir = experiment_dir / "eval_outputs"

    parser.add_argument(
        "--mode",
        choices=["workflow", "agent", "both", "eval"],
        default="both",
        help="Execution mode. Default runs both workflow and agent on a small sample.",
    )
    parser.add_argument(
        "--samples",
        type=Path,
        default=default_data_dir / "samples.jsonl",
        help="Path to samples JSONL.",
    )
    parser.add_argument(
        "--gold",
        type=Path,
        default=default_data_dir / "gold.jsonl",
        help="Path to gold JSONL (used by eval mode).",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=default_output_dir,
        help="Output directory for eval artifacts.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Max number of sample rows to run for workflow/agent/both modes.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.mode == "eval":
        result = run_eval(samples_path=args.samples, gold_path=args.gold, output_dir=args.out)
        print(
            {
                "mode": "eval",
                "corpus_size": result["summary"]["corpus_size"],
                "summary_json": result["summary_json"],
                "summary_md": result["summary_md"],
                "predictions_csv": result["predictions_csv"],
            }
        )
        return

    samples = _read_jsonl(args.samples, limit=args.limit)

    if args.mode in {"workflow", "agent"}:
        _run_per_case(samples, mode=args.mode)
        return

    _run_per_case(samples, mode="workflow")
    _run_per_case(samples, mode="agent")


if __name__ == "__main__":
    main()
