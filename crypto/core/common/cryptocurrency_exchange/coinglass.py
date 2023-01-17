from crypto import settings
from crypto.core.api.api import CoinGlassApi


class CoinGlassTracking:
    def __init__(self):
        self.api_key = settings.COIN_GLASS_API_KEY

    def get_funding_rate(self):
        """
        Docs: https://coinglass.readme.io/reference/funding-rate
        """
        endpoint = "funding"
        coin_glass_api = CoinGlassApi(
            service_endpoint=endpoint,
            api_key=self.api_key,
        )()
        return coin_glass_api.status_code, coin_glass_api.result
