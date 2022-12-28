from crypto.core.common.tracking.etherscan import EtherscanTracking


class EtherscanService:
    def get_contact_verify(self):
        etherscan_tracking = EtherscanTracking()
        status, result = etherscan_tracking.get_contact_abi_for_verified_contact_source_code(
            "0xBB9bc244D798123fDe783fCc1C72d3Bb8C189413")
        print(status, result)

        return result
