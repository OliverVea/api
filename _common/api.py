import abc
import json
from typing import Any, Callable

import urlpath

from api._common.response import Response
from api.headers.header import Headers


class Api(abc.ABC):
    def __init__(self,
                 base_url: str | urlpath.URL,
                 verify: bool = False,
                 constant_headers: dict[str, str] | Headers | None = None):
        
        self.base_url = base_url
        self.verify = verify
        self.headers = Headers(constant_headers)

    def _get_headers(self, extra_headers: dict[str, str] | Headers | None) -> Headers:
        headers = Headers(self.headers)
        headers += Headers(self._get_authorization_headers())
        headers += Headers(extra_headers)
        return headers
    
    def _get_url(self, path: str) -> urlpath.URL:
        return self.base_url / path

    @abc.abstractmethod
    def _get_authorization_headers(self) -> dict[str, str] | Headers | None:
        raise NotImplementedError()
    
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

        return Response(url, response=response, content=content, json=content_json, exception=exception)

    def get(self,
            path: str,
            params: Any | None = None,
            headers: dict[str, str] | Headers | None = None) -> Response:
        
        url: urlpath.URL = self.base_url / path

        headers = self._get_headers(headers).to_dict()

        request = lambda: url.get(params=params, verify=self.verify, headers=headers)
        return self._get_response(url, request)

    def post(self,
             path: str,
             data,
             params: Any | None = None,
             headers: dict[str, str] | Headers | None = None) -> Response:
        
        url: urlpath.URL = self.base_url / path

        headers = self._get_headers(headers).to_dict()

        request = lambda: url.post(data=data, params=params, verify=self.verify, headers=headers)
        return self._get_response(url, request)

    def put(self,
            path: str,
            data,
            params: Any | None = None,
            headers: dict[str, str] | Headers | None = None) -> Response:
        
        url: urlpath.URL = self.base_url / path

        headers = self._get_headers(headers).to_dict()

        request = lambda: url.put(data=data, params=params, verify=self.verify, headers=headers)
        return self._get_response(url, request)

    def delete(self,
               path: str,
               params: Any | None = None,
               headers: dict[str, str] | Headers | None = None) -> Response:
        
        url: urlpath.URL = self.base_url / path

        headers = self._get_headers(headers).to_dict()

        request = lambda: url.delete(params=params, verify=self.verify, headers=headers)
        return self._get_response(url, request)

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
            if response.json:
                print(json.dumps(response.json, indent=4))
            elif response.succeeded():
                print(response.content.encode('utf-8'))
            else:
                print(f'{response.response.status_code}: {response.response.reason}')

        return response