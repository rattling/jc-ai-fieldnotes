from pydantic import BaseModel


class AgentResult(BaseModel):
	mode: str
	steps: int