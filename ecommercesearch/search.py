import base64
import requests

from api._common.api import Api
from api.ecommercesearch.config import EcommerceSearchConfiguration
from api.headers.header import bearer_token_authorization, content_type_json, accept_json, Headers

class SearchApi(Api):
    def __init__(self, config: EcommerceSearchConfiguration, print_swagger: bool = True, verify: bool = False):
        super().__init__(config.search_url, verify, content_type_json() + accept_json())
        self.config = config

        if print_swagger:
            print(f'Search API Swagger: {self.base_url / "swagger/index.html"}')
        
    def _get_authorization_headers(self) -> dict[str, str] | Headers | None:
        return None

