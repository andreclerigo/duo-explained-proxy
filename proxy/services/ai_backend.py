from services.backends.chatgpt import ChatGPTBackend
# from services.backends.local_model import LocalModelBackend

class AIBackend:
    """
    Middleware that abstracts calls to different backend implementations.
    """

    def __init__(self, backend_type: str = "openai", api_key: str = None):
        self.backend_type = backend_type
        self.api_key = api_key

        if backend_type == "openai":
            self.backend = ChatGPTBackend(api_key)
        # elif backend_type == "local":
        #     self.backend = LocalModelBackend()
        else:
            raise ValueError(f"Unknown backend type: {backend_type}")

    def get_response(self, prompt: str) -> str:
        """
        Forwards request to selected backend.
        """
        return self.backend.get_response(prompt)
