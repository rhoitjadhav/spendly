from base_agent import BaseAgent
from common.utils import to_dict
from core.llm import get_llm
from sql_builder.constants import SQLBUILDER_AGENT_SYSTEM_PROMPT
from sql_builder.schemas import SQLBuilderAgentResponse
from common.schemas import ModelQueryRequest
from langchain_core.messages import HumanMessage, SystemMessage


class SQLBuilderAgent(BaseAgent):
    name = "sql_builder"
    system_prompt = SQLBUILDER_AGENT_SYSTEM_PROMPT
    model = "deepseek-coder"  # llama2 zephyr openchat orca2

    def __init__(self):
        self.llm = get_llm(self.model)

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
