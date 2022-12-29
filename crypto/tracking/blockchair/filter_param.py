from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter

token_address = OpenApiParameter(
    'token_address',
    OpenApiTypes.STR,
    OpenApiParameter.QUERY,
    description='',
    required=True
)

holder_address = OpenApiParameter(
    'holder_address',
    OpenApiTypes.STR,
    OpenApiParameter.QUERY,
    description=''
)

time_ago = OpenApiParameter(
    'time_ago',
    OpenApiTypes.INT,
    OpenApiParameter.QUERY,
    description='time ago minute'
)

min_order_exchange = OpenApiParameter(
    'min_order_exchange',
    OpenApiTypes.INT,
    OpenApiParameter.QUERY,
    description='time ago minute'
)

exchange_id = OpenApiParameter(
    'exchange_id',
    OpenApiTypes.STR,
    OpenApiParameter.QUERY,
    description='exchange_id: binance, bybit, mexc'
)
name_exchange = OpenApiParameter(
    'name_exchange',
    OpenApiTypes.STR,
    OpenApiParameter.QUERY,
    description='exchange_id: Binance 14'
)
