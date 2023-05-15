import abc
from typing import Any

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
    
    @abc.abstractmethod
    def get(self,
            path: str,
            params: Any | None = None,
            headers: dict[str, str] | Headers | None = None) -> Response:
        
        raise NotImplementedError()

    @abc.abstractmethod
    def post(self,
             path: str,
             data,
             params: Any | None = None,
             headers: dict[str, str] | Headers | None = None) -> Response:
        raise NotImplementedError()

    @abc.abstractmethod
    def put(self,
            path: str,
            data,
            params: Any | None = None,
            headers: dict[str, str] | Headers | None = None) -> Response:
        raise NotImplementedError()

    @abc.abstractmethod
    def delete(self,
               path: str,
               params: Any | None = None,
               headers: dict[str, str] | Headers | None = None) -> Response:
        raise NotImplementedError()
