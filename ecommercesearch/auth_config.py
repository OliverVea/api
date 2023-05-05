import dataclasses

@dataclasses.dataclass
class AuthConfiguration:
    clientId: str
    clientSecret: str
    auth: str