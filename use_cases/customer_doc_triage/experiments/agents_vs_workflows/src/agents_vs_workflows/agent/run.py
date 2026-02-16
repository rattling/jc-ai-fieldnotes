from customer_doc_triage.agent.pipeline import run_agentic


def main() -> None:
	decision = run_agentic(
		{
			"doc_id": "DOC-DEMO-AGENT",
			"channel": "email",
			"customer_id": "CUST-DEMO",
			"customer_tier": "enterprise",
			"region": "EU",
			"submitted_at": "2026-02-16T12:00:00Z",
			"doc_type_hint": "access request",
			"content": "Need temporary privileged admin access for contractor in regulated account.",
			"metadata": {
				"requested_role": "admin",
				"justification": "migration window",
				"approval_reference": "CHG-200",
			},
		}
	)
	print(decision.model_dump())


if __name__ == "__main__":
	main()