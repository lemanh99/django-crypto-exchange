from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from crypto.coinglass.services import CoinGlassService
from crypto.core.response import make_response


# Create your views here.
@extend_schema(
    methods=['GET'],
    tags=['coinglass'],
    description='',
    summary='',
    responses={200: {}},
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_funding_rate(request):
    coin_glass_service = CoinGlassService()
    data = coin_glass_service.get_funding_rate_exchange_crypto()
    return make_response(data=data, app_status=200)
