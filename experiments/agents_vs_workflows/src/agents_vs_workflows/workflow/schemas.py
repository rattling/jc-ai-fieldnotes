from pydantic import BaseModel


class WorkflowResult(BaseModel):
	mode: str
	status: str