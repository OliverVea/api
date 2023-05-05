import dataclasses

@dataclasses.dataclass
class ChatGPTResponse:
    prompt: str
    response: str
    full_response: dict