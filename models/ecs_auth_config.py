import dataclasses

@dataclasses.dataclass
class ECSAuthConfig:
    clientId: str
    clientSecret: str
    auth: str