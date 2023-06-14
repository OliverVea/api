import base64
import time
import requests

from api._common.api import Api
from api.ecommercesearch.bearer_token import BearerToken
from api.ecommercesearch.config import EcommerceSearchConfiguration
from api.headers.header import bearer_token_authorization, content_type_json, accept_json, Headers


class AdminApi(Api):
    def __init__(self, config: EcommerceSearchConfiguration, print_swagger: bool = True, verify: bool = False):
        super().__init__(config.admin_url, verify, content_type_json() + accept_json())
        self.config = config
        self.token = self._get_bearer_token()

        if print_swagger:
            print(f'Admin API Swagger: {self.base_url / "swagger/index.html"}')
    
    def _get_bearer_token(self) -> BearerToken:
        url = self.config.auth_url / 'connect/token'

        authorization = base64.b64encode(bytes(self.config.client_id + ":" + self.config.client_secret, "ISO-8859-1")).decode("ascii")

        headers = {
            "Authorization": f"Basic {authorization}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        body = {
            "grant_type": "client_credentials",
            "scope": 'searchapi/'
        }

        response = requests.post(url, data=body, headers=headers, verify=False).json()

        return BearerToken(response['access_token'], response['expires_in'])
        
    def _get_authorization_headers(self) -> dict[str, str] | Headers | None:
        if self.token == None or self.token.is_expired():
            self.token = self._get_bearer_token()

        return bearer_token_authorization(self.token.token)
    
    def wait_for_publication(self, segment: str, publication_comment: str = '', attempts_before: int = 10, sleep_before: float = 0.2, attempts_after: int = 20, sleep_after: float = 5):
        for _ in range(attempts_before):
            before_response = self.post(f'/api/segments/{segment}/publication/validate-summary', {}).json

            if before_response['publicationAllowed']:
                break

            time.sleep(sleep_before)

        else:
            raise TimeoutError()
        
        publication_response = self.post(f'/api/segments/{segment}/publication/publish', 
        {
            'comment': publication_comment
        }).json

        for _ in range(attempts_after):
            before_response = self.post(f'/api/segments/{segment}/publication/validate-summary', {}).json

            if before_response['isValidationUptoDate']:
                break

            time.sleep(sleep_after)

        else:
            raise TimeoutError()


