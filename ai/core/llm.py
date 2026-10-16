import os
from abc import ABC, abstractmethod
from ollama import Client
from anthropic import Anthropic
from mistralai.client import Mistral
from openai import OpenAI
from pydantic import BaseModel
from core.constants import ModelProvider
from langchain.chat_models import init_chat_model


class BaseLLM(ABC):
    @abstractmethod
    def chat(self, messages: list[dict], system: str = "") -> str: ...


class AnthropicLLM(BaseLLM):
    def __init__(self):
        self._client = Anthropic()
        self.model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")

    def chat(
        self,
        messages: list[dict],
        system: str = "",
        max_tokens: float = 1024,
        response_model: type[BaseModel] = None,
    ) -> str:
        res = self._client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system,
            messages=messages,
            response_model=response_model,
        )
        return res.content[0].text


class MistralLLM(BaseLLM):
    def __init__(self):
        self._client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
        self.model = os.getenv("MISTRAL_MODEL", "mistral-large-latest")

    def chat(self, messages: list[dict], system: str = "") -> str:
        res = self._client.chat.complete(model=self.model, messages=messages)
        return res.choices[0].message.content


class OpenAILLM(BaseLLM):
    def __init__(self):
        self._client = OpenAI()
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o")

    def chat(self, messages: list[dict], system: str = "") -> str:
        res = self._client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": system}, *messages]
        )
        return res.choices[0].message.content


class OllamaLLM(BaseLLM):
    def __init__(self, model: str = "llama3.2"):
        self._client = Client(
            host=os.getenv("OLLAMA_HOST", "http://localhost:11434")
        )
        self.model = os.getenv("OLLAMA_MODEL", model)

    def chat(
        self,
        messages: list[dict],
        system: str = "",
        format: dict = None,
        options: dict = None,
    ) -> str:
        res = self._client.chat(
            model=self.model,
            messages=[{"role": "system", "content": system}, *messages],
            format=format,
            options=options,
        )
        return res["message"]["content"]


_PROVIDERS: dict[str, type[BaseLLM]] = {
    "anthropic": AnthropicLLM,
    "mistral": MistralLLM,
    "openai": OpenAILLM,
    "ollama": OllamaLLM,
}


def get_llm(model) -> BaseLLM:
    provider = os.getenv("LLM_PROVIDER", "ollama")
    cls = _PROVIDERS.get(provider)
    if not cls:
        raise ValueError(
            f"Unknown LLM_PROVIDER={provider!r}. Choose: {list(_PROVIDERS)}"
        )
    return cls(model)


class LLM:
    def __init__(model: str, provider: ModelProvider, temperatur: float = 1):
        self._llm_client = init_chat_model(
            model, model_provider=provider, temperature=temperature
        )

    def get_llm_client():
        return self._llm_client

    def with_structured_output(pydantic_model: type[BaseModel]):
        return self._llm_client.with_structured_output(pydantic_model)
