import base64
import dataclasses
import json
import requests

import urllib3
urllib3.disable_warnings()

@dataclasses.dataclass
class AuthorizationConfiguration:
    clientId: str
    clientSecret: str
    auth: str

class EcommerceSearch:
    def __init__(self, host: str, config: AuthorizationConfiguration):
        self.host = host
        self.token = self._get_bearer_token(config)
    
    def _get_bearer_token(self, config: AuthorizationConfiguration) -> str:
        url = f'{config.auth}/connect/token'

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
    
    def _get_url(self, endpoint: str):
        return f'{self.host}{endpoint}'
    
    def _get_headers(self, additional_headers: dict[str, str]) -> dict[str, str]:
        headers = {}
        headers['Authorization'] = f'Bearer {self.token}'
        headers['Content-Type'] = 'application/json'

        for key, val in additional_headers.items():
            headers[key] = val

        return headers
    
    def post(self, endpoint: str, data, params: dict[str,str] = {}, additional_headers: dict[str, str] = {}):
        url = self._get_url(endpoint)
        headers = self._get_headers(additional_headers)

        response = requests.post(url, data=data, params=params, headers=headers, verify=False)

        try:
            return response.json()
        except json.JSONDecodeError:
            return None
    
    def get(self, endpoint: str, params: dict[str, str] = {}, additional_headers: dict[str, str] = {}):
        url = self._get_url(endpoint)
        headers = self._get_headers(additional_headers)

        response = requests.get(url, params=params, headers=headers, verify=False)

        try:
            return response.json()
        except json.JSONDecodeError:
            print(f'Could not decode JSON got ({response.status_code}):\n{response.content.decode("utf-8")}')
            return None