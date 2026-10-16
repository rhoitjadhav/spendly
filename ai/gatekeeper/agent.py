from base_agent import BaseAgent
from common.utils import to_dict
from core.llm import get_llm
from gatekeeper.constants import GATEKEEPER_AGENT_SYSTEM_PROMPT
from gatekeeper.schemas import GatekeeperAgentResponse
from common.schemas import ModelQueryRequest

class GatekeeperAgent(BaseAgent):
    name = "gatekeeper"
    system_prompt = GATEKEEPER_AGENT_SYSTEM_PROMPT
    model = "zephyr"  # llama2 zephyr openchat orca2
    provider = ModelProvider.OLLAMA

    def __init__(self):
        self._llm_client = LLM(self.model, self.provider).get_llm_client()

    async def run(self, content: ModelQueryRequest) -> dict:
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=content.query)
        ]

        structured_llm = self._llm_client.with_structured_output(
            GatekeeperAgentResponse
        )
        reply = structured_llm.invoke(messages)

        return reply["parsed"]
