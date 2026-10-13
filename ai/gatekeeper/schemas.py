from typing import Optional

from pydantic import BaseModel


class GatekeeperChatRequest(BaseModel):
    query: str


class GatekeeperAgentResponse(BaseModel):
    action: str
    confidence: float
    reason: str
    category: str
    clarification_needed: Optional[str]
    user_id: Optional[str]
