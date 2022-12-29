from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter

token_address = OpenApiParameter(
    'token_address',
    OpenApiTypes.STR,
    OpenApiParameter.QUERY,
    description=''
)

holder_address = OpenApiParameter(
    'holder_address',
    OpenApiTypes.STR,
    OpenApiParameter.QUERY,
    description=''
)