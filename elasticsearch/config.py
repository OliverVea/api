import dataclasses
import urlpath

@dataclasses.dataclass
class ElasticsearchConfiguration:
    base_url: urlpath.URL = urlpath.URL('https://localhost:9200')
    username: str | None = 'elastic'
    password: str | None = 'ELASTIC_PASSWORD'