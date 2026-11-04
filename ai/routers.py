from common.schemas import ChatResponse, ModelQueryRequest
from fastapi import APIRouter
from fastapi.params import Depends
from planner.agent import PlannerAgent
from planner.schemas import (
    ActionEnum,
    GatekeeperAgentResponse,
)
from synthesizer.agent import SQLBuilderAgent

router = APIRouter(prefix="/api/v1", tags=["Gatekeeper"])


@router.post("/chat")
async def chat(
    payload: ModelQueryRequest,
    planner_agent: PlannerAgent = Depends(PlannerAgent),  # noqa: B008
):
    return await planner_agent.run(payload)
