from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_200_OK

from crypto.core.response import make_response
from crypto.user.serializers import UserTelegramTrackerSerializer, UserTokenTriggerSerializer
from crypto.user.services import UserService


# Create your views here.
@extend_schema(
    methods=['GET'],
    tags=['user'],
    responses={HTTP_200_OK: {}},
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_telegram_tracker_by_user_id(request, user_id):
    user_service = UserService()
    data = user_service.get_user_telegram_tracker_by_user_id(user_id)
    return make_response(data=data, app_status=200)


@extend_schema(
    methods=['POST'],
    tags=['user'],
    request=UserTelegramTrackerSerializer,
    responses={HTTP_200_OK: {}},
)
@api_view(['POST'])
@permission_classes([AllowAny])
def create_action_tracking_telegram(request):
    user_service = UserService()
    data = user_service.create_action_tracking_telegram(request.data)
    return make_response(data=data, app_status=200)


@extend_schema(
    methods=['PUT'],
    tags=['user'],
    request=UserTelegramTrackerSerializer,
    responses={HTTP_200_OK: {}},
)
@api_view(['PUT'])
@permission_classes([AllowAny])
def update_user_telegram_tracker_by_user_id(request, user_id):
    user_service = UserService()
    data = user_service.update_user_telegram_tracker_by_user_id(user_id, request.data)
    return make_response(data=data, app_status=200)


@extend_schema(
    methods=['DELETE'],
    tags=['user'],
    responses={HTTP_200_OK: {}},
)
@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_user_telegram_tracker_by_user_id(request, user_id):
    user_service = UserService()
    data = user_service.delete_user_telegram_tracker_by_user_id(user_id)
    return make_response(data=data, app_status=200)


@extend_schema(
    methods=['DELETE'],
    tags=['user'],
    responses={HTTP_200_OK: {}},
)
@api_view(['DELETE'])
@permission_classes([AllowAny])
def clear_data_user_telegram_tracker(request):
    user_service = UserService()
    data = user_service.clear_data_user_telegram_tracker()
    return make_response(data=data, app_status=200)

@extend_schema(
    methods=['GET'],
    tags=['user'],
    responses={HTTP_200_OK: {}},
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_list_token_trigger(request):
    user_service = UserService()
    data = user_service.get_list_token_trigger()
    return make_response(data=data, app_status=200)

@extend_schema(
    methods=['GET'],
    tags=['user'],
    responses={HTTP_200_OK: {}},
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_list_token_trigger_running_by_user_id(request, user_id):
    user_service = UserService()
    data = user_service.get_list_token_trigger_running_by_user_id(user_id)
    return make_response(data=data, app_status=200)


@extend_schema(
    methods=['POST'],
    tags=['user'],
    request=UserTokenTriggerSerializer,
    responses={HTTP_200_OK: {}},
)
@api_view(['POST'])
@permission_classes([AllowAny])
def create_token_trigger_by_user(request):
    user_service = UserService()
    data = user_service.create_token_trigger_by_user(request.data)
    return make_response(data=data, app_status=200)


@extend_schema(
    methods=['PUT'],
    tags=['user'],
    responses={HTTP_200_OK: {}},
)
@api_view(['PUT'])
@permission_classes([AllowAny])
def stop_running_by_user_id_and_token(request, user_id):
    user_service = UserService()
    data = user_service.update_status_running_by_user_id(user_id)
    return make_response(data=data, app_status=200)

@extend_schema(
    methods=['DELETE'],
    tags=['user'],
    responses={HTTP_200_OK: {}},
)
@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_token_trigger_by_user_id(request, user_id, token):
    user_service = UserService()
    data = user_service.delete_token_trigger_by_user_id(user_id, token)
    return make_response(data=data, app_status=200)