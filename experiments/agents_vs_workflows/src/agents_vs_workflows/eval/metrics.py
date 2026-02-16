from __future__ import annotations

from collections import defaultdict
from statistics import mean
from typing import Any


def accuracy(predictions: list[dict[str, Any]], gold: dict[str, dict[str, Any]], field: str) -> float:
	total = len(predictions)
	if total == 0:
		return 0.0

	correct = 0
	for prediction in predictions:
		doc_id = prediction["doc_id"]
		if doc_id in gold and prediction.get(field) == gold[doc_id].get(field):
			correct += 1

	return correct / total


def escalation_precision_recall(
	predictions: list[dict[str, Any]], gold: dict[str, dict[str, Any]]
) -> tuple[float, float]:
	true_positive = 0
	false_positive = 0
	false_negative = 0

	for prediction in predictions:
		doc_id = prediction["doc_id"]
		if doc_id not in gold:
			continue

		pred_escalate = bool(prediction.get("escalate", False))
		gold_escalate = bool(gold[doc_id].get("escalate", False))

		if pred_escalate and gold_escalate:
			true_positive += 1
		elif pred_escalate and not gold_escalate:
			false_positive += 1
		elif not pred_escalate and gold_escalate:
			false_negative += 1

	precision = true_positive / (true_positive + false_positive) if (true_positive + false_positive) else 0.0
	recall = true_positive / (true_positive + false_negative) if (true_positive + false_negative) else 0.0
	return precision, recall


def missing_field_recall(predictions: list[dict[str, Any]], gold: dict[str, dict[str, Any]]) -> float:
	recalls: list[float] = []

	for prediction in predictions:
		doc_id = prediction["doc_id"]
		if doc_id not in gold:
			continue

		pred_missing = set(prediction.get("required_missing_fields", []))
		gold_missing = set(gold[doc_id].get("required_missing_fields", []))

		if not gold_missing:
			recalls.append(1.0)
			continue

		recalls.append(len(pred_missing & gold_missing) / len(gold_missing))

	return mean(recalls) if recalls else 0.0


def latency_and_cost_proxies(predictions: list[dict[str, Any]]) -> dict[str, float]:
	if not predictions:
		return {"avg_elapsed_ms": 0.0, "avg_tool_calls": 0.0}

	elapsed = [float(pred.get("decision_trace", {}).get("elapsed_ms", 0)) for pred in predictions]
	tool_calls = [float(pred.get("decision_trace", {}).get("tool_calls", 0)) for pred in predictions]

	return {
		"avg_elapsed_ms": mean(elapsed),
		"avg_tool_calls": mean(tool_calls),
	}


def edge_case_flag(gold_row: dict[str, Any]) -> bool:
	return bool(gold_row.get("escalate", False) or gold_row.get("required_missing_fields"))


def slice_summary(
	predictions: list[dict[str, Any]], gold: dict[str, dict[str, Any]]
) -> dict[str, dict[str, float | int]]:
	by_doc_type: dict[str, list[dict[str, Any]]] = defaultdict(list)
	by_edge_case: dict[str, list[dict[str, Any]]] = defaultdict(list)

	for prediction in predictions:
		doc_id = prediction["doc_id"]
		if doc_id not in gold:
			continue

		gold_row = gold[doc_id]
		by_doc_type[str(gold_row.get("true_doc_type", "unknown"))].append(prediction)
		by_edge_case["edge_case" if edge_case_flag(gold_row) else "non_edge_case"].append(prediction)

	summary: dict[str, dict[str, float | int]] = {}

	for label, rows in by_doc_type.items():
		summary[f"doc_type:{label}"] = {
			"count": len(rows),
			"doc_type_accuracy": accuracy(rows, gold, field="doc_type"),
			"queue_accuracy": accuracy(rows, gold, field="recommended_queue"),
		}

	for label, rows in by_edge_case.items():
		summary[f"slice:{label}"] = {
			"count": len(rows),
			"doc_type_accuracy": accuracy(rows, gold, field="doc_type"),
			"queue_accuracy": accuracy(rows, gold, field="recommended_queue"),
		}

	return summary


def score(predictions: list[dict[str, Any]], gold: dict[str, dict[str, Any]]) -> dict[str, Any]:
	escalation_precision, escalation_recall = escalation_precision_recall(predictions, gold)
	proxies = latency_and_cost_proxies(predictions)

	return {
		"doc_type_accuracy": accuracy(predictions, gold, field="doc_type"),
		"queue_accuracy": accuracy(predictions, gold, field="recommended_queue"),
		"escalation_precision": escalation_precision,
		"escalation_recall": escalation_recall,
		"missing_field_recall": missing_field_recall(predictions, gold),
		"avg_elapsed_ms": proxies["avg_elapsed_ms"],
		"avg_tool_calls": proxies["avg_tool_calls"],
		"slices": slice_summary(predictions, gold),
	}