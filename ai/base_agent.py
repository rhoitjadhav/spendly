from abc import ABC, abstractmethod
from typing import Any

from common.schemas import ModelQueryRequest


class BaseAgent(ABC):
    name: str
    system_prompt: str
    model: str
    provider: str

    @abstractmethod
    async def run(self, content: ModelQueryRequest) -> Any:
        pass
