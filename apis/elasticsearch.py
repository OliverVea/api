from typing import Any

import json
import urlpath
import base64

from models.elasticsearch_configuration import ElasticsearchConfiguration
from models.elasticsearch_response import ElasticsearchResponse

class Elasticsearch:
    def __init__(self, config: ElasticsearchConfiguration, verify: bool = False):
        self.config = config
        self.verify = verify
        self.headers = {'Accept': 'application/json'}

    def _get_headers(self, extra_headers: dict[str, str] | None) -> dict[str, str]:
        headers = {'Authorization': f'Basic {self._get_token()}'}

        headers.update(self.headers)
        if extra_headers: headers.update(extra_headers)

        return headers

    def _get_token(self):
        token_content = f'{self.config.username}:{self.config.password}'
        token_content_bytes = token_content.encode('utf-8')
        token = base64.b64encode(token_content_bytes)
        return token.decode('ascii')

    def _get_content(self, response: urlpath.requests.Response) -> tuple[str | None , Any | None]:
        content = content_json = None

        try:
            content = response.content.decode('utf-8')
            content_json = json.loads(content)

        except Exception:
            pass

        return content, content_json

    def get(self, path: str, params: Any | None = None, headers: Any | None = None) -> ElasticsearchResponse:
        url = self.config.base_url / path

        headers = self._get_headers(headers)

        try:
            response = url.get(params=params, verify=self.verify, headers=headers)

        except Exception as exception:
            print(f'Got exception:\n{exception}')
            return ElasticsearchResponse(self.config, url, exception=exception)

        content, content_json = self._get_content(response)

        return ElasticsearchResponse(self.config, url, response=response, content=content, json=content_json)
