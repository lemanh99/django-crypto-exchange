from crypto import settings
from crypto.core.api.api import EtherscanApi

class EtherscanTracking:
    def __init__(self):
        self.api_key = settings.ETHERSCAN_API_KEY

    def get_contact_abi_for_verified_contact_source_code(self, address_contact):
        """
        Docs: https://docs.etherscan.io/api-endpoints/contracts
        """
        endpoint = "api"
        params = dict(
            module="contract",
            action="getabi",
            address=address_contact,
        )
        etherscan_api = EtherscanApi(
            service_endpoint=endpoint,
            api_key=self.api_key,
            params=params
        )()
        return etherscan_api.status_code, etherscan_api.result
