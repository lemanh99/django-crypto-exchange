from rest_framework import status
from rest_framework.response import Response

from crypto.core.exceptions.api_exception import CryptoBaseException


def make_response(app_status, data=None):
    try:
        if data is None:
            data = {}

        return Response(status=app_status, data=data)
    except CryptoBaseException as ex:
        raise ex
    except Exception as error:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=dict(error))
