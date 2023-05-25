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

    def _get_authorization_headers(self) -> dict[str, str] | Headers | None:
        if not self.config.username or not self.config.password:
            return None
        
        return basic_authorization(self.config.username, self.config.password)
