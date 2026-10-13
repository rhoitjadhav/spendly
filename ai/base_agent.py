from abc import ABC, abstractmethod


class BaseAgent(ABC):
    name: str
    system_prompt: str

    @abstractmethod
    async def run(self, input: dict) -> dict:
        pass
