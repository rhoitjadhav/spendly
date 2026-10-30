from enum import StrEnum

from pydantic import BaseModel, Field


class GatekeeperChatRequest(BaseModel):
    query: str


class ActionEnum(StrEnum):
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"
    CLARIFY = "CLARIFY"


class CategoryEnum(StrEnum):
    SPENDING = "spending"
    CATEGORY = "category"
    MERCHANT = "merchant"
    APP = "app"
    PATTERN = "pattern"
    COMPARISON = "comparison"
    SECURITY = "security"
    OUT_OF_SCOPE = "out-of-scope"
    AMBIGUOUS = "ambiguous"


class GatekeeperAgentResponse(BaseModel):
    """
    Evaluates a user request to determine the next platform action,
    confidence score, classification category, and context details.
    """

    action: ActionEnum = Field(description="The primary action to take on the request.")
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="How certain you are about this decision. Only use 1.0 if you are 100% certain.",
    )
    reason: str = Field(
        description="The specific, non-generic justification for this action. Limit to 1 sentence maximum."
    )
    category: CategoryEnum = Field(
        description="The functional category or domain the user's intent falls into."
    )
    user_id: str | None
    clarification_needed: str | None = Field(
        default=None,
        description="The question or prompt to send back to the user. Only fill this if action is CLARIFY, otherwise null.",
    )
