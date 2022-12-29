from abc import ABC

import requests
from django.conf import settings
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

from crypto.core.exceptions.api_exception import CryptoServiceException


class BaseApiProxy(ABC):
    def __init__(self):
        self.api_name = None
        self.service_uri = None
        self.method = None
        self.headers = None
        self.params = None
        self.data = None
        self.json = None

    def __call__(self, **kwargs):
        try:
            resp = requests.request(
                url=self.service_uri,
                method=self.method,
                headers=self.headers,
                params=self.params,
                data=self.data,
                json=self.json,
                **kwargs
            )
            self.status_code = resp.status_code
            self.result = resp.json()
            if (
                    self.method in ["PUT", "POST", "DELETE"]
                    and self.status_code
                    not in [HTTP_200_OK, HTTP_201_CREATED, ]
            ):
                message = "{} exception: status {}, message: {} ".format(
                    self.api_name,
                    self.status_code,
                    self.result.get("message", "Can not get message"),
                )
                if "detail" in self.result:
                    message += ", detail: {}".format(self.result.get("detail"))

                raise CryptoServiceException(
                    message_code=message,
                    status_code=self.status_code,
                )
            return self
        except Exception as ex:
            raise CryptoServiceException(message_code=repr(ex))


class EtherscanApi(BaseApiProxy):
    def __init__(
            self,
            service_endpoint,
            method="GET",
            headers=None,
            params=None,
            data=None,
            json=None,
            api_key=None,
    ):
        super().__init__()
        self.api_name = "Etherscan"
        self.service_uri = "https://api.etherscan.io" + "/" + service_endpoint
        self.method = method
        self.headers = headers
        self.params = dict(**params, apikey=api_key) if params else dict(apikey=api_key)
        self.data = data
        self.json = json
        self.result = None
        self.status_code = HTTP_200_OK


class BlockchairApi(BaseApiProxy):
    def __init__(
            self,
            service_endpoint,
            method="GET",
            headers=None,
            params=None,
            data=None,
            json=None,
            api_key=None,
    ):
        super().__init__()
        self.api_name = "Blockchair"
        self.service_uri = "https://api.blockchair.com" + "/" + service_endpoint
        self.method = method
        self.headers = headers
        # self.params = dict(**params, key=api_key) if params else dict(key=api_key)
        self.data = data
        self.json = json
        self.result = None
        self.status_code = HTTP_200_OK
