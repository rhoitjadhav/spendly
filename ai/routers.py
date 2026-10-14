from fastapi import APIRouter
from fastapi.params import Depends

from gatekeeper.agent import GatekeeperAgent
from gatekeeper.schemas import GatekeeperChatRequest, GatekeeperAgentResponse

router = APIRouter(prefix="/api/v1", tags=["Gatekeeper"])


@router.post("/chat")
async def chat(
    payload: GatekeeperChatRequest,
    gatekeeper_agent: GatekeeperAgent = Depends(GatekeeperAgent)
) -> GatekeeperAgentResponse:
    response = await gatekeeper_agent.run(payload)
    if response.action in [ActionEnum.REJECT, ActionEnum.CLARIFY]:
        return response
