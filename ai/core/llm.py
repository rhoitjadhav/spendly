from core.constants import ModelProvider
from langchain.chat_models import init_chat_model
from pydantic import BaseModel


class LLM:
    def __init__(self, model: str, provider: ModelProvider, temperature: float = 1):
        self._llm_client = init_chat_model(
            model, model_provider=provider, temperature=temperature
        )

    def get_llm_client(self):
        return self._llm_client

    def with_structured_output(self, pydantic_model: type[BaseModel]):
        return self._llm_client.with_structured_output(pydantic_model)
