from base_agent import BaseAgent
from common.utils import to_dict
from core.llm import get_llm
from gatekeeper.constants import GATEKEEPER_AGENT_SYSTEM_PROMPT
from gatekeeper.schemas import GatekeeperChatRequest, GatekeeperAgentResponse


class GatekeeperAgent(BaseAgent):
    name = "gatekeeper"
    system_prompt = GATEKEEPER_AGENT_SYSTEM_PROMPT
    model = "zephyr"  # llama2 zephyr openchat orca2

    def __init__(self):
        self.llm = get_llm(self.model)

    async def run(self, content: GatekeeperChatRequest) -> dict:
        reply = self.llm.chat(
            messages=[{"role": "user", "content": content.query}],
            system=self.system_prompt,
            format=GatekeeperAgentResponse.model_json_schema(),
            options={"temperature": 0}
        )
        return GatekeeperAgentResponse(**to_dict(reply.message.content))
