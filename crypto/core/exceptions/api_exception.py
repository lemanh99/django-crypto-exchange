from rest_framework import status
from rest_framework.exceptions import APIException


class CryptoBaseException(APIException):
    def __init__(
            self,
            detail="Common error",
            status_code=status.HTTP_400_BAD_REQUEST,
            message_code=None,
    ):
        self.detail = {"detail": detail, "message_code": message_code}
        self.status_code = status_code


class CryptoSystemException(CryptoBaseException):
    def __init__(
            self,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="System error",
            message_code=None,
    ):
        super(CryptoSystemException, self).__init__(status_code, detail, message_code)


class CryptoServiceException(CryptoBaseException):
    def __init__(
            self,
            detail="Service error!",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            message_code=None,
    ):
        super(CryptoServiceException, self).__init__(detail, status_code, message_code)
