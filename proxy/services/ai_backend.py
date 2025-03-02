from services.backends.chatgpt import ChatGPTBackend
from config import get_next_api_key

class AIBackend:
    """
    Middleware that abstracts calls to different backend implementations.
    """

    def __init__(self, backend_type: str = "openai"):
        self.backend_type = backend_type

        if backend_type == "openai":
            self.backend = ChatGPTBackend()
        else:
            raise ValueError(f"Unknown backend type: {backend_type}")

    def get_response(self, prompt: str) -> str:
        """
        Forwards request to selected backend, using rotating API keys.
        """
        return self.backend.get_response(prompt, api_key=get_next_api_key())
