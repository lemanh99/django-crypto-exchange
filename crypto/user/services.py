import uuid
from datetime import datetime, timezone

from django.db import transaction, DatabaseError

from crypto.user.models import UserTelegramTracker
from crypto.user.serializers import UserTelegramTrackerSerializer


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
