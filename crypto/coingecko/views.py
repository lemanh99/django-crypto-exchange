from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from crypto.coingecko.filter_params import exchange_ids, target_pairs
from crypto.coingecko.services import CoinGeckoService
from crypto.core.common.filter_params import symbol
from crypto.core.response import make_response


# Create your views here.
@extend_schema(
    methods=['GET'],
    tags=['coingecko'],
    parameters=[symbol, exchange_ids, target_pairs],
    description='',
    summary='',
    responses={200: {}},
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_percent_market_exchange(request):
    cg_service = CoinGeckoService()
    data = cg_service.get_percent_market_exchange(request.GET)
    return make_response(data=data, app_status=200)
