from api.ecommercesearch.admin import AdminApi
from api.ecommercesearch.search import SearchApi
from api.ecommercesearch.config import EcommerceSearchConfiguration

from pathlib import Path

def get_clients(path: str | Path) -> tuple[EcommerceSearchConfiguration, AdminApi, SearchApi]:
    config = EcommerceSearchConfiguration.load(path)
    admin = AdminApi(config)
    search = SearchApi(config)

    return config, admin, search