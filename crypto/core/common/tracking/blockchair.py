from crypto import settings
from crypto.core.api.api import BlockchairApi


class BlockChairTracking:
    def __init__(self):
        self.api_key = settings.BLOCKCHAIR_API_KEY

    def get_history_transaction_holder_erc20_token(
            self,
            token_address,
            holder_address,
            limit=50,
            offset=0
    ):
        """
        Docs: https://blockchair.com/api/docs#link_503
        """
        endpoint = f"ethereum/erc-20/{token_address}/dashboards/address/{holder_address}"
        params = dict(
            limit=limit,
            offset=offset
        )
        blockchair_api = BlockchairApi(
            service_endpoint=endpoint,
            api_key=self.api_key,
            params=params
        )()
        return blockchair_api.status_code, blockchair_api.result
