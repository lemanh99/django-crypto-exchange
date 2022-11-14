from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter

symbol = OpenApiParameter(
    'symbol',
    OpenApiTypes.STR,
    OpenApiParameter.QUERY,
    description='Symbol token: BTC, ETH')