from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

Channel = Literal["email", "portal", "attachment", "api"]
CustomerTier = Literal["enterprise", "growth", "standard"]
Region = Literal["NA", "EU", "APAC", "LATAM"]
DocType = Literal[
    "incident_report",
    "access_request",
    "security_questionnaire",
    "billing_dispute",
    "feature_request",
]
Priority = Literal["P1", "P2", "P3"]
TriageMode = Literal["workflow", "agent"]


class TriageInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    doc_id: str = Field(min_length=1)
    channel: Channel
    customer_id: str = Field(min_length=1)
    customer_tier: CustomerTier | None = None
    region: Region
    submitted_at: datetime
    doc_type_hint: str | None = None
    content: str = Field(min_length=1)
    metadata: dict[str, Any] = Field(default_factory=dict)


class DecisionTrace(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mode: TriageMode
    steps: list[str] = Field(default_factory=list)
    tool_calls: int = Field(default=0, ge=0)
    retry_count: int = Field(default=0, ge=0)
    elapsed_ms: int = Field(default=0, ge=0)
    model_name: str | None = None


class TriageDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    doc_id: str = Field(min_length=1)
    doc_type: DocType
    priority: Priority
    severity_score: int = Field(ge=1, le=5)
    recommended_queue: str = Field(min_length=1)
    required_missing_fields: list[str] = Field(default_factory=list)
    escalate: bool
    escalation_reason: str | None = None
    confidence: float = Field(ge=0.0, le=1.0)
    rationale: str = Field(min_length=1)
    decision_trace: DecisionTrace

    @model_validator(mode="after")
    def validate_escalation_reason(self) -> "TriageDecision":
        if self.escalate and not self.escalation_reason:
            raise ValueError("escalation_reason is required when escalate=true")
        if not self.escalate and self.escalation_reason is not None:
            raise ValueError("escalation_reason must be null when escalate=false")
        return self