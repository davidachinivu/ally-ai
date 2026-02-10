from abc import ABC, abstractmethod
from llm_client import LLMClient

class BaseAgent(ABC):
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    @abstractmethod
    def process(self, *args, **kwargs):
        pass
