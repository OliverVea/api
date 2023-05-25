import base64
import requests

from api._common.api import Api
from api.ecommercesearch.config import EcommerceSearchConfiguration
from api.headers.header import bearer_token_authorization, content_type_json, accept_json, Headers

class EcommerceSearchSearch(Api):
    def __init__(self, config: EcommerceSearchConfiguration, verify: bool = False):
        super().__init__(config.search_url, verify, content_type_json() + accept_json())
        self.config = config
        
    def _get_authorization_headers(self) -> dict[str, str] | Headers | None:
        return None

