from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomJWTAuthentication(JWTAuthentication):
    TYPE = "http"
    SCHEME = "bearer"
    BEARER_FORMAT = settings.AUTH_HEADER_TYPES
    keyword = "Token"
