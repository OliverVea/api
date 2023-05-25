from api._common.response import Response
from api.ecommercesearch.config import EcommerceSearchConfiguration

class EcommerceSearchResponse(Response):
    config: EcommerceSearchConfiguration | None = None

    def __init__(self, response: Response, config: EcommerceSearchConfiguration):
        for name, value in response.to_dict().items():
            self.__setattr__(name, value)

        self.config = config