from base_agent import BaseAgent
from common.utils import to_dict
from core.llm import get_llm
from sql_builder.constants import SQLBUILDER_AGENT_SYSTEM_PROMPT
from sql_builder.schemas import SQLBuilderAgentResponse
from common.schemas import ModelQueryRequest


class SQLBuilderAgent(BaseAgent):
    name = "sql_builder"
    system_prompt = SQLBUILDER_AGENT_SYSTEM_PROMPT
    model = "deepseek-coder"  # llama2 zephyr openchat orca2

    def __init__(self):
        self.llm = get_llm(self.model)

    async def run(self, content: ModelQueryRequest) -> dict:
        reply = self.llm.chat(
            messages=[{"role": "user", "content": content.query}],
            system=self.system_prompt,
            format=SQLBuilderAgentResponse.model_json_schema(),
            options={"temperature": 0}
        )
        return GatekeeperAgentResponse(**to_dict(reply.message.content))
