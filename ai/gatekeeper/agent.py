from base_agent import BaseAgent
from common.schemas import ModelQueryRequest
from common.utils import to_dict
from core.constants import ModelProvider
from core.llm import LLM
from gatekeeper.constants import GATEKEEPER_AGENT_SYSTEM_PROMPT
from gatekeeper.schemas import ActionEnum, GatekeeperAgentResponse
from langchain_core.messages import HumanMessage, SystemMessage


class GatekeeperAgent(BaseAgent):
    name = "gatekeeper"
    system_prompt = GATEKEEPER_AGENT_SYSTEM_PROMPT
    model = "zephyr:7b"  # llama2 zephyr:7b openchat orca2
    provider = ModelProvider.OLLAMA

    def __init__(self):
        self._llm_client = LLM(self.model, self.provider).get_llm_client()

    async def run(self, content: ModelQueryRequest) -> GatekeeperAgentResponse:
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=content.query),
        ]

        structured_llm = self._llm_client.with_structured_output(
            GatekeeperAgentResponse
        )
        reply = structured_llm.invoke(messages)

        return reply
