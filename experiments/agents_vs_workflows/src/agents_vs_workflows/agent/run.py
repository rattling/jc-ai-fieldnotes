from agents_vs_workflows.agent.planner import plan


def main() -> None:
	steps = plan("demo")
	print({"mode": "agent", "steps": len(steps)})


if __name__ == "__main__":
	main()