from rest_framework import serializers

from crypto.user.models import UserTelegramTracker, UserTokenTrigger


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


class UserTokenTriggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTokenTrigger
        fields = (
            'user_id',
            'name',
            'symbol',
            'address',
            'running',
        )
