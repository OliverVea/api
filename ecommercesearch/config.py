import dataclasses
import urlpath

@dataclasses.dataclass
class EcommerceSearchConfiguration:
    admin_url: urlpath.URL = urlpath.URL('https://ecommercesearch.bzk.hdk')
    search_url: urlpath.URL = urlpath.URL('https://search.bzk.hdk')
    auth_url: urlpath.URL = urlpath.URL('https://auth.bzk.hdk')
    clientId: str = 'search-internal'
    clientSecret: str = 'search-internal-secret'

    def __post_init__(self):
        if isinstance(self.admin_url, str):
            self.admin_url = urlpath.URL(self.admin_url)

        if isinstance(self.search_url, str):
            self.search_url = urlpath.URL(self.search_url)

        if isinstance(self.auth_url, str):
            self.auth_url = urlpath.URL(self.auth_url)
