from abc import ABC, abstractmethod

class BaseAIBackend(ABC):
    @abstractmethod
    def get_response(self, prompt: str) -> str:
        pass
