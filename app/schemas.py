from enum import Enum

from pydantic import BaseModel, Field


class Intent(str, Enum):
    create_appointment = "create_appointment"
    cancel_appointment = "cancel_appointment"
    reschedule_appointment = "reschedule_appointment"
    business_question = "business_question"
    human_handoff = "human_handoff"
    unknown = "unknown"


class AgentRequest(BaseModel):
    message: str = Field(min_length=2, max_length=2000)
    customer_id: str | None = Field(default=None, max_length=100)


class AgentResponse(BaseModel):
    intent: Intent
    confidence: float = Field(ge=0, le=1)
    reply: str
    requires_human: bool
    next_action: str
    matched_terms: list[str]
