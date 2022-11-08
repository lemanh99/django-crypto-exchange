import logging
import traceback

from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import exception_handler as rest_exception_handler
from rest_framework.views import set_rollback

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = rest_exception_handler(exc, context)
    exc_fmt = traceback.format_exc()
    logger.error(exc_fmt)
    # Now add the HTTP status code to the response.
    if response is not None:
        response.data["status_code"] = response.status_code
    else:
        set_rollback()
        if isinstance(exc, ValueError):
            data = {"detail": f"Value Error: {str(exc)}"}
            status_code = 400
        else:
            data = {"detail": f"Server Error: {str(exc)}"}
            status_code = 500
        if settings.DEBUG:
            data["exception"] = repr(exc)
            data["traceback"] = exc_fmt
        return Response(data, status=status_code)

    return response
