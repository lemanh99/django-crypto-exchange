from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication

__all__ = [
    'CustomJWTAuthentication',
]


class CustomJWTAuthentication(JWTAuthentication):
    TYPE = "https"
    SCHEME = "bearer"
    BEARER_FORMAT = settings.AUTH_HEADER_TYPES
    keyword = "Token"
