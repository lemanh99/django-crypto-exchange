from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from crypto.binance.services import BinanceService
from crypto.core.common.cryptocurrency_exchange.binance import BinanceCryptoExchangeFutures
from crypto.core.response import make_response


# Create your views here.
@extend_schema(
    methods=['GET'],
    tags=['binance'],
    description='',
    summary='',
    responses={200: {}},
)
@api_view(['GET'])
@permission_classes([AllowAny])
def binance_account_information(request):
    binance_service = BinanceService()
    data = binance_service.get_account_information()
    return make_response(data=data, app_status=200)


@extend_schema(
    methods=['GET'],
    tags=['binance'],
    description='',
    summary='',
    responses={200: {}},
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_funding_rate_binance(request):
    binance_service = BinanceService()
    data = binance_service.get_funding_rate_binance()
    return make_response(data=data, app_status=200)
