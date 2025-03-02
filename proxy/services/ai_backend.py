# services/ai_backend.py

import os
import requests
from typing import Optional

# If you plan to use OpenAI:
# import openai

# from config import OPENAI_API_KEY

class AIBackend:
    """
    An example AI backend class that can be adapted to different providers.
    """

    def __init__(self, backend_type: str = "openai", api_key: Optional[str] = None):
        self.backend_type = backend_type
        self.api_key = api_key  # For OpenAI or other providers

        # If using openai
        # if self.backend_type == "openai" and self.api_key:
        #     openai.api_key = self.api_key

    def get_response(self, prompt: str) -> str:
        """
        Retrieves an AI-generated response given a user prompt.
        Adjust this method to match your chosen backend’s API calls.
        """

        if self.backend_type == "openai":
            return self._handle_openai(prompt)

        # If you have some local model or another endpoint:
        # elif self.backend_type == "my_local_model":
        #     return self._handle_local_model(prompt)

        return "No valid backend configured."

    def _handle_openai(self, prompt: str) -> str:
        # Example using OpenAI's ChatCompletion endpoint
        # import openai
        # response = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=[{"role": "user", "content": prompt}]
        # )
        # return response["choices"][0]["message"]["content"]
        return "(mock) This is where you'd call the OpenAI API, e.g., ChatCompletion."

    def _handle_local_model(self, prompt: str) -> str:
        # Example placeholder for local model integration
        return "(mock) This is where you'd query your local LLM."
