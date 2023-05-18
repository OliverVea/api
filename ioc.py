from api.elasticsearch.api import Elasticsearch
from api.elasticsearch.config import ElasticsearchConfiguration

from ioc import ioc

def register_apis(elastic_config: ElasticsearchConfiguration | None = None):
    if elastic_config:
        elasticsearch = Elasticsearch(elastic_config)
        ioc.add_instance(elastic_config, ElasticsearchConfiguration)
        ioc.add_instance(elasticsearch, Elasticsearch)