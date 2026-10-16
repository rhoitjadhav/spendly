from base_agent import BaseAgent
from common.schemas import ModelQueryRequest
from core.constants import ModelProvider
from core.llm import LLM
from langchain_core.messages import HumanMessage, SystemMessage
from sql_builder.constants import SQLBUILDER_AGENT_SYSTEM_PROMPT
from sql_builder.schemas import SQLBuilderAgentResponse


class SQLBuilderAgent(BaseAgent):
    name = "sql_builder"
    system_prompt = SQLBUILDER_AGENT_SYSTEM_PROMPT
    model = "deepseek-coder"  # llama2 zephyr openchat orca2
    provider = ModelProvider.OLLAMA

    def __init__(self):
        self._llm_client = LLM(self.model, self.provider).get_llm_client()

    async def run(self, content: ModelQueryRequest) -> dict:
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=content.query),
        ]

        structured_llm = self._llm_client.with_structured_output(
            SQLBuilderAgentResponse
        )
        reply = structured_llm.invoke(messages)

        return reply["parsed"]
