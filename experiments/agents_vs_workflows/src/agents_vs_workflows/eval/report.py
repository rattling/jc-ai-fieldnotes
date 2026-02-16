from __future__ import annotations

import argparse
from pathlib import Path

from agents_vs_workflows.eval.harness import run_eval


def main() -> None:
	parser = argparse.ArgumentParser(description="Run A/B replay evaluation for agents_vs_workflows.")
	default_data_dir = Path(__file__).resolve().parents[3] / "data"
	default_output_dir = Path(__file__).resolve().parents[3] / "eval_outputs"

	parser.add_argument("--samples", type=Path, default=default_data_dir / "samples.jsonl")
	parser.add_argument("--gold", type=Path, default=default_data_dir / "gold.jsonl")
	parser.add_argument("--out", type=Path, default=default_output_dir)
	args = parser.parse_args()

	result = run_eval(samples_path=args.samples, gold_path=args.gold, output_dir=args.out)
	print(
		{
			"corpus_size": result["summary"]["corpus_size"],
			"summary_json": result["summary_json"],
			"summary_md": result["summary_md"],
			"predictions_csv": result["predictions_csv"],
		}
	)


if __name__ == "__main__":
	main()