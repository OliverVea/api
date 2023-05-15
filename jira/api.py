import dataclasses
from typing import Any, Callable
import json
import urlpath

from api._common.api import Api
from api._common.response import Response
from api.headers.header import Headers, basic_authorization, bearer_token_authorization, content_type_json
from api.jira.config import JiraConfiguration

class JiraResponse(Response):
    config: JiraConfiguration | None = None

    def __init__(self, response: Response, config: JiraConfiguration):
        for name, value in response.to_dict().items():
            self.__setattr__(name, value)

        self.config = config

@dataclasses.dataclass
class JiraSearchResponseIssue:
    id: str
    key: str
    expand: str
    self: str
    fields: dict[str, str]

@dataclasses.dataclass
class JiraSearchResponse():
    expand: str
    start: int
    max_results: int
    total: int
    issues: list[JiraSearchResponseIssue]
    response: JiraResponse



class Jira(Api):
    def __init__(self, config: JiraConfiguration, verify: bool = False):
        super().__init__(config.base_url, verify, content_type_json())
        self.config = config

    def _get_authorization_headers(self) -> dict[str, str] | Headers | None:
        return basic_authorization('olve@bizzkit.com', self.config.token)
    
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

        return JiraResponse(
            response=Response(url, response=response, content=content, json=content_json, exception=exception),
            config=self.config)

    def get(self, path: str, params: Any | None = None, headers: dict[str, str] | Headers | None = None):
        url = self.base_url / path

        headers = self._get_headers(headers).to_dict()

        request = lambda: url.get(params=params, verify=self.verify, headers=headers)
        return self._get_response(url, request)
    
    def post(self, path: str, data, params: Any | None = None, headers: dict[str, str] | Headers | None = None):
        return super().post(path, data, params, headers)
    
    def put(self, path: str, data, params: Any | None = None, headers: dict[str, str] | Headers | None = None):
        return super().put(path, data, params, headers)
    
    def delete(self, path: str, params: Any | None = None, headers: dict[str, str] | Headers | None = None):
        return super().delete(path, params, headers)
    


    def search(self, jql: str, fields: list[str] = None, start: int = 0, max_results: int = 1000000):
        params = {
            'jql': jql,
            'fields': fields,
            'startAt': start,
            'maxResults': max_results
        }

        response = self.get(f'rest/api/2/search', params=params)

        issues = [JiraSearchResponseIssue(**issue) for issue in response.json['issues']]

        return JiraSearchResponse(
            response=response,
            expand=response.json['expand'],
            max_results=response.json['maxResults'],
            start=response.json['startAt'],
            total=response.json['total'],
            issues=issues
        )
