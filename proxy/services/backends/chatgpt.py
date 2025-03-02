import requests

class ChatGPTBackend:
    """
    Backend handler for OpenAI's ChatGPT.
    """

    def __init__(self):
        self.url = "https://api.openai.com/v1/chat/completions"

    def get_response(self, prompt: str, api_key: str) -> str:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}]
        }

        response = requests.post(self.url, json=payload, headers=headers)

        if response.status_code != 200:
            return f"Error from OpenAI: {response.status_code} - {response.text}"

        data = response.json()
        return data['choices'][0]['message']['content']
