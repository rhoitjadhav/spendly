from ai.base_agent import BaseAgent
from ai.common.schemas import ModelQueryRequest
from ai.core.constants import ModelProvider
from ai.core.llm import LLM
from ai.synthesizer.constants import SQLBUILDER_AGENT_SYSTEM_PROMPT
from ai.synthesizer.schemas import SQLBuilderAgentResponse
from langchain_core.messages import HumanMessage, SystemMessage


class SQLBuilderAgent(BaseAgent):
    name = "sql_builder"
    system_prompt = SQLBUILDER_AGENT_SYSTEM_PROMPT
    model = "deepseek-coder"  # llama2 zephyr openchat orca2
    provider = ModelProvider.OLLAMA

    def __init__(self):
        self._llm_client = LLM(self.model, self.provider).get_llm_client()

    async def run(self, content: ModelQueryRequest) -> SQLBuilderAgentResponse:
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=content.query),
        ]

        structured_llm = self._llm_client.with_structured_output(
            SQLBuilderAgentResponse
        )
        reply = structured_llm.invoke(messages)

        return reply["parsed"]
