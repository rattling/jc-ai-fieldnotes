from agents_vs_workflows.eval.metrics import score


def main() -> None:
	print({"metric": score()})


if __name__ == "__main__":
	main()