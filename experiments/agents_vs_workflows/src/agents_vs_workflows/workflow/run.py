from agents_vs_workflows.workflow.pipeline import run_workflow


def main() -> None:
	decision = run_workflow(
		{
			"doc_id": "DOC-DEMO-WF",
			"channel": "portal",
			"customer_id": "CUST-DEMO",
			"customer_tier": "enterprise",
			"region": "EU",
			"submitted_at": "2026-02-16T12:00:00Z",
			"doc_type_hint": "access request",
			"content": "Please grant temporary admin access for migration.",
			"metadata": {
				"requested_role": "admin",
				"justification": "migration",
			},
		}
	)
	print(decision.model_dump())


if __name__ == "__main__":
	main()