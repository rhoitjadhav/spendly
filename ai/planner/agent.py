from datetime import datetime, timedelta

from base_agent import BaseAgent
from common.schemas import ModelQueryRequest
from core.constants import ModelProvider
from core.llm import LLM
from langchain_core.messages import HumanMessage, SystemMessage, ToolCall
from planner.constants import PLANNER_AGENT_SYSTEM_PROMPT
from planner.schemas import IST, DateContext, GatekeeperAgentResponse
from tools import default_tools, lending_tools, transaction_tools


class PlannerAgent(BaseAgent):
    name = "planner"
    system_prompt = PLANNER_AGENT_SYSTEM_PROMPT
    model = "llama3.2"  # llama2 zephyr:7b openchat orca2
    provider = ModelProvider.OLLAMA

    def __init__(self):
        self._llm_client = LLM(self.model, self.provider).get_llm_client()

    def _format_planner_prompt(self) -> str:
        """Defaults to 'now' in IST — servers run UTC, and 'this month'
        must match the user's calendar at midnight."""

        today = datetime.now(IST).date()
        month_start = today.replace(day=1)
        prev_month_end = month_start - timedelta(days=1)
        prev_month_start = prev_month_end.replace(day=1)
        ctx = DateContext(today, month_start, prev_month_start, prev_month_end)

        return (
            self.system_prompt.replace("{today}", ctx.today.isoformat())
            .replace("{month_start}", ctx.month_start.isoformat())
            .replace("{prev_month_start}", ctx.prev_month_start.isoformat())
            .replace("{prev_month_end}", ctx.prev_month_end.isoformat())
        )

    async def run(self, content: ModelQueryRequest) -> list[ToolCall]:
        messages = [
            SystemMessage(content=self._format_planner_prompt()),
            HumanMessage(content=content.query),
        ]

        bind_tools = self._llm_client.bind_tools(
            tools=transaction_tools + lending_tools + default_tools
        )
        reply = bind_tools.invoke(messages)
        return reply.tool_calls
