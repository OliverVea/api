import dataclasses
import urlpath

from typing import Any

from models.elasticsearch_configuration import ElasticsearchConfiguration

@dataclasses.dataclass
class ElasticsearchResponse:
    config: ElasticsearchConfiguration
    url: urlpath.URL
    response: urlpath.requests.Response | None = None
    content: str | None = None
    json: Any | None = None
    exception: Exception | None = None

    def succeeded(self):
        if self.exception != None:
            return False
        
        if self.response == None:
            return True
        
        if self.response.status_code < 200 or self.response.status_code > 299:
            return False
        
        return True
