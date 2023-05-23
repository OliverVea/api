from typing import Any, Callable

import json
import urlpath

from api._common.api import Api
from api.elasticsearch.config import ElasticsearchConfiguration
from api._common.response import Response
from api.headers.header import Headers, accept_json, basic_authorization, content_type_json

class ElasticResponse(Response):
    config: ElasticsearchConfiguration | None = None

    def __init__(self, response: Response, config: ElasticsearchConfiguration):
        for name, value in response.to_dict().items():
            self.__setattr__(name, value)

        self.config = config

class Elasticsearch(Api):
    def __init__(self, config: ElasticsearchConfiguration, verify: bool = False):
        super().__init__(config.base_url, verify, content_type_json() + accept_json())
        self.config = config
    
    def _get_response(self, url: urlpath.URL, request: Callable):
        response = exception = content = content_json = None

        try:
            response: urlpath.requests.Response = request()

        except Exception as e:
            exception = e
            print(f'Got exception:\n{exception}')

        try:
            content = response.content.decode('utf-8')
            content_json = json.loads(content)

        except Exception:
            pass

        return ElasticResponse(
            response=Response(url, response=response, content=content, json=content_json, exception=exception),
            config=self.config)

    def _get_authorization_headers(self) -> dict[str, str] | Headers | None:
        if not self.config.username or not self.config.password:
            return None
        
        return basic_authorization(self.config.username, self.config.password)

    def get(self, 
            path: str, 
            params: Any | None = None, 
            headers: dict[str, str] | Headers | None = None) -> ElasticResponse:
        
        url: urlpath.URL = self.base_url / path

        headers = self._get_headers(headers).to_dict()

        request = lambda: url.get(params=params, verify=self.verify, headers=headers)
        return self._get_response(url, request)
    
    def post(self, 
             path: str, 
             data, 
             params: Any | None = None, 
             headers: dict[str, str] | Headers | None = None) -> ElasticResponse:
        
        url: urlpath.URL = self.base_url / path

        headers = self._get_headers(headers).to_dict()

        request = lambda: url.post(data=data, params=params, verify=self.verify, headers=headers)
        return self._get_response(url, request)
    
    def put(self, path: str, data, params: Any | None = None, headers: dict[str, str] | Headers | None = None) -> ElasticResponse:
        
        url: urlpath.URL = self.base_url / path

        headers = self._get_headers(headers).to_dict()

        request = lambda: url.put(data=data, params=params, verify=self.verify, headers=headers)
        return self._get_response(url, request)
    
    def delete(self, path: str, params: Any | None = None, headers: dict[str, str] | Headers | None = None) -> ElasticResponse:
        return super().delete(path, params, headers)

    def _breakdown_request(self, request: str) -> tuple[str, str]:
        method, *uri = request.split(' ')
        method = method.lower()
        uri = ' '.join(uri)
        return method, uri

    def eval(self, request: str, body: dict | None = None, print_response: bool = True):
        method_name, uri = self._breakdown_request(request)

        method = {'post': self.post, 'get': self.get, 'put': self.put, 'delete': self.delete}[method_name]
        uri = urlpath.URL(uri)

        if method_name in ('post', 'put'):
            if body:
                body = json.dumps(body)

            response: Response = method(uri.path, body, params=uri.form_fields)

        else:
            response: Response = method(uri.path, params=uri.form_fields)

        if print_response:
            print(json.dumps(response.json, indent=4))

        return response
