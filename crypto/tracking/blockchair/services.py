from crypto.core.common.tracking.blockchair import BlockChairTracking


class BlockchairService:
    def get_history_transaction(self, req_data):
        token_address = req_data.get("token_address")
        holder_address = req_data.get("holder_address")
        etherscan_tracking = BlockChairTracking()
        status, result = etherscan_tracking.get_history_transaction_holder_erc20_token(
            token_address=token_address,
            holder_address=holder_address
        )
        return result["data"].get(holder_address)
