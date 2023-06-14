import dataclasses
import time

class BearerToken:
    token: str
    expiry: float
    
    def __init__(self, token: str, expiry: float):
        self.token = token
        self.expiry = time.time() + expiry
    
    def is_expired(self) -> bool:
        return time.time() > self.expiry
    
    def __str__(self) -> str:
        return self.token