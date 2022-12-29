from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from crypto.core.response import make_response
from crypto.tracking.blockchair.filter_param import token_address, holder_address
from crypto.tracking.blockchair.services import BlockchairService


# Create your views here.
@extend_schema(
    methods=['GET'],
    tags=['blockchair'],
    parameters=[token_address, holder_address],
    description='',
    summary='',
    responses={200: {}},
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_history_transaction(request):
    blockchair_service = BlockchairService()
    data = blockchair_service.get_history_transaction(request.GET)
    return make_response(data=data, app_status=200)