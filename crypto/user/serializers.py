from rest_framework import serializers

from crypto.user.models import UserTelegramTracker


class UserTelegramTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTelegramTracker
        fields = (
            'user_id',
            'username',
            'step_current',
            'commands',
            'text_input',
            'create_date',
            'expired_date'
        )
