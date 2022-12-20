from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter

exchange_ids = OpenApiParameter(
    'exchange_ids',
    OpenApiTypes.STR,
    OpenApiParameter.QUERY,
    default='binance,mxc,uniswap_v2,uniswap_v3,uniswap_v3_arbitrum,huobi,gate',
    description='exchange_ids: binance, mxc, uniswap_v2, uniswap_v3, uniswap_v3_arbitrum, huobi, gate'
)
target_pairs = OpenApiParameter(
    'target_pairs',
    OpenApiTypes.STR,
    OpenApiParameter.QUERY,
    default='USDT,BUSD',
    description=''
)
