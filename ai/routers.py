from common.schemas import ChatResponse, ModelQueryRequest
from fastapi import APIRouter
from fastapi.params import Depends
from planner.agent import GatekeeperAgent
from planner.schemas import (
    ActionEnum,
    GatekeeperAgentResponse,
)
from synthesizer.agent import SQLBuilderAgent

router = APIRouter(prefix="/api/v1", tags=["Gatekeeper"])


@router.post("/chat")
async def chat(
    payload: ModelQueryRequest,
    gatekeeper_agent: GatekeeperAgent = Depends(GatekeeperAgent),  # noqa: B008
    sql_builder_agent: SQLBuilderAgent = Depends(SQLBuilderAgent),  # noqa: B008
) -> GatekeeperAgentResponse:
    response = await gatekeeper_agent.run(payload)
    if response.action in [ActionEnum.REJECT, ActionEnum.CLARIFY]:
        return response

    response = await sql_builder_agent.run(payload)
    if not response.is_feasible:
        return response

    return ChatResponse()
