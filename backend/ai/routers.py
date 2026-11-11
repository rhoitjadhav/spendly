from ai.common.schemas import ModelQueryRequest
from ai.planner.agent import PlannerAgent
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/api/v1", tags=["Gatekeeper"])


@router.post("/chat")
async def chat(
    payload: ModelQueryRequest,
    planner_agent: PlannerAgent = Depends(PlannerAgent),  # noqa: B008
):
    return await planner_agent.run(payload)
