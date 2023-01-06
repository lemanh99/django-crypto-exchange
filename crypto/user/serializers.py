from rest_framework import serializers

from crypto.user.models import UserTelegramTracker


class UserTelegramTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTelegramTracker
        fields = ('user_id', 'username', 'uuid', 'token_tracker')
