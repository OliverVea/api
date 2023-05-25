import base64
import requests

from api._common.api import Api
from api.ecommercesearch.config import EcommerceSearchConfiguration
from api.headers.header import bearer_token_authorization, content_type_json, accept_json, Headers

class EcommerceSearchAdmin(Api):
    def __init__(self, config: EcommerceSearchConfiguration, verify: bool = False):
        super().__init__(config.admin_url, verify, content_type_json() + accept_json())
        self.config = config
        self.token = self._get_bearer_token(config)
    
    def _get_bearer_token(self, config: EcommerceSearchConfiguration) -> str:
        url = config.auth_url / 'connect/token'

        authorization = base64.b64encode(bytes(config.clientId + ":" + config.clientSecret, "ISO-8859-1")).decode("ascii")

        headers = {
            "Authorization": f"Basic {authorization}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        body = {
            "grant_type": "client_credentials",
            "scope": 'searchapi/'
        }

        response = requests.post(url, data=body, headers=headers, verify=False).json()

        return response['access_token']
        
    def _get_authorization_headers(self) -> dict[str, str] | Headers | None:
        return bearer_token_authorization(self.token)

