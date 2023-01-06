import uuid
from datetime import datetime, timezone

from django.db import transaction, DatabaseError

from crypto.user.models import UserTelegramTracker
from crypto.user.serializers import UserTelegramTrackerSerializer


class UserService:
    @classmethod
    def get_user_telegram_tracker_by_uuid(cls, uuid):
        try:
            user_telegram = UserTelegramTracker.objects.get(uuid=uuid)
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
                req_data['uuid'] = str(uuid.uuid4().hex)
                user_tracker_serializer = UserTelegramTrackerSerializer(data=req_data)
                user_tracker_serializer.is_valid(raise_exception=True)
                user_tracker_serializer.save()

            return user_tracker_serializer.data
        except DatabaseError:
            return dict(error="Database error")
        except Exception as e:
            return dict(error=str(e))

    @classmethod
    def delete_user_telegram_tracker_by_uuid(cls, uuid):
        try:
            UserTelegramTracker.objects.filter(uuid=uuid).delete()
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
