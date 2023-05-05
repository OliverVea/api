import json
import os
import requests

import urllib3
urllib3.disable_warnings()

from models.chatgpt_response import ChatGPTResponse

class ChatGPT:
    def __init__(self, max_tokens: int = 2000, temperature: float = 0.5):
        self.api_key = os.environ['OPENAI_USER_AFFINITIES_KEY']
        self.max_tokens = max_tokens
        self.temperature = temperature

        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.api_key
        }

    def _get_data(self, prompt: str) -> dict:
        return {
            'prompt': prompt,
            'max_tokens': self.max_tokens,
            'temperature': self.temperature
        }
    
    def _get_url(self, model: str = 'text-davinci-003'):
        return f'https://api.openai.com/v1/engines/{model}/completions'

    def get_answer(self, prompt: str) -> ChatGPTResponse:
        url = self._get_url()
        data = self._get_data(prompt)

        response = requests.post(url, headers=self.headers, data=json.dumps(data))
        response_json = response.json()

        return ChatGPTResponse(prompt, response_json['choices'][0]['text'], response)