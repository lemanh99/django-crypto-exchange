from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from crypto.coingecko.filter_params import exchange_ids, target_pairs, max_market_cap, number_pages
from crypto.coingecko.services import CoinGeckoService
from crypto.core.common.filter_params import symbol
from crypto.core.response import make_response
from crypto.tracking.etherscan.services import EtherscanService


# Create your views here.
@extend_schema(
    methods=['GET'],
    tags=['etherscan'],
    parameters=[],
    description='',
    summary='',
    responses={200: {}},
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_contact_verify(request):
    ether_service = EtherscanService()
    data = ether_service.get_contact_verify()
    return make_response(data=data, app_status=200)