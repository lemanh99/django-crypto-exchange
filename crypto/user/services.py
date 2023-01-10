import uuid
from datetime import datetime, timezone

from django.db import transaction, DatabaseError

from crypto.core.utils.dict import get_unique_list_of_dict
from crypto.user.models import UserTelegramTracker, UserTokenTrigger
from crypto.user.serializers import UserTelegramTrackerSerializer, UserTokenTriggerSerializer


class UserService:
    @classmethod
    def get_user_telegram_tracker_by_user_id(cls, user_id):
        try:
            user_telegram = UserTelegramTracker.objects.get(user_id=user_id)
            return UserTelegramTrackerSerializer(user_telegram).data
        except UserTelegramTracker.DoesNotExist:
            return None
        except DatabaseError:
            return dict(error="Database error")
        except Exception as e:
            return dict(error=str(e))

    @classmethod
    def create_action_tracking_telegram(cls, req_data):
        try:
            with transaction.atomic():
                user_tracker_serializer = UserTelegramTrackerSerializer(data=req_data)
                user_tracker_serializer.is_valid(raise_exception=True)
                user_tracker_serializer.save()

            return user_tracker_serializer.data
        except DatabaseError:
            return dict(error="Database error")
        except Exception as e:
            return dict(error=str(e))

    @classmethod
    def delete_user_telegram_tracker_by_user_id(cls, user_id):
        try:
            UserTelegramTracker.objects.filter(user_id=user_id).delete()
        except DatabaseError:
            return dict(error="Database error")
        except Exception as e:
            return dict(error=str(e))

    @classmethod
    def update_user_telegram_tracker_by_user_id(cls, user_id, req_data):
        try:
            user_telegram = UserTelegramTracker.objects.get(user_id=user_id)
            user_tracker_serializer = UserTelegramTrackerSerializer(instance=user_telegram, data=req_data)
            user_tracker_serializer.is_valid(raise_exception=True)
            user_tracker_serializer.save()
        except UserTelegramTracker.DoesNotExist:
            return dict(error="User not found")
        except DatabaseError:
            return dict(error="Database error")
        except Exception as e:
            return dict(error=str(e))

    @classmethod
    def clear_data_user_telegram_tracker(cls):
        try:
            UserTelegramTracker.objects.filter(expired_date__lte=datetime.now(tz=timezone.utc)).delete()
        except DatabaseError:
            return dict(error="Database error")
        except Exception as e:
            return dict(error=str(e))

    @classmethod
    def create_token_trigger_by_user(cls, req_data):
        try:
            with transaction.atomic():
                user_trigger_serializer = UserTokenTriggerSerializer(data=req_data)
                user_trigger_serializer.is_valid(raise_exception=True)
                user_trigger_serializer.save()

            return user_trigger_serializer.data
        except DatabaseError:
            return dict(error="Database error")
        except Exception as e:
            return dict(error=str(e))

    @classmethod
    def get_list_token_trigger_running_by_user_id(cls, user_id):
        try:
            token_trigger = UserTokenTrigger.objects.filter(user_id=user_id, running__in=[1, True])
            return UserTokenTriggerSerializer(token_trigger, many=True).data
        except UserTokenTrigger.DoesNotExist:
            return None
        except DatabaseError:
            return dict(error="Database error")
        except Exception as e:
            return dict(error=str(e))

    @classmethod
    def get_list_token_trigger(cls):
        try:
            token_trigger = UserTokenTrigger.objects.all()
            return get_unique_list_of_dict(UserTokenTriggerSerializer(token_trigger, many=True).data)
        except UserTokenTrigger.DoesNotExist:
            return None
        except DatabaseError:
            return dict(error="Database error")
        except Exception as e:
            return dict(error=str(e))

    @classmethod
    def update_status_running_by_user_id(cls, user_id, running=False):
        try:
            UserTokenTrigger.objects.filter(user_id=user_id).update(running=running)
        except UserTokenTrigger.DoesNotExist:
            return dict(error="User and token not found")
        except DatabaseError:
            return dict(error="Database error")
        except Exception as e:
            return dict(error=str(e))

    @classmethod
    def delete_token_trigger_by_user_id(cls, user_id, token):
        try:
            UserTelegramTracker.objects.filter(user_id=user_id, token=token).delete()
        except DatabaseError:
            return dict(error="Database error")
        except Exception as e:
            return dict(error=str(e))
