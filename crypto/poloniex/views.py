from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from crypto.core.common.filter_params import symbol
from crypto.core.response import make_response
from crypto.poloniex.services import PoloniexService


# Create your views here.
@extend_schema(
    methods=['GET'],
    tags=['poloniex'],
    parameters=[symbol],
    description='',
    summary='',
    responses={200: {}},
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_pair_trade_arbitrage(request):
    poloniex_service = PoloniexService()
    data = poloniex_service.get_pair_trade_arbitrage(request.GET)
    return make_response(data=data, app_status=200)


@extend_schema(
    methods=['GET'],
    tags=['poloniex'],
    description='',
    summary='',
    responses={200: {}},
)
@api_view(['GET'])
@permission_classes([AllowAny])
def trade_arbitrage(request):
    poloniex_service = PoloniexService()
    data = poloniex_service.trade_arbitrage(request.GET)
    return make_response(data=data, app_status=200)
