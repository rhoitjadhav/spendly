from fastapi import APIRouter
from fastapi.params import Depends

from gatekeeper.agent import GatekeeperAgent
from gatekeeper.schemas import GatekeeperChatRequest, GatekeeperAgentResponse

router = APIRouter(prefix="/api/v1", tags=["Gatekeeper"])


@router.post("/query")
async def query(
    payload: GatekeeperChatRequest,
    agent: GatekeeperAgent = Depends(GatekeeperAgent)
) -> GatekeeperAgentResponse:
    return await agent.run(payload)
