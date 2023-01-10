from rest_framework import serializers

from crypto.tracking.blockchair.models import BlockchairRequest


class BlockchairRequestSerializer(serializers.ModelSerializer):
    remaining_request = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BlockchairRequest
        fields = (
            'user_login',
            'total',
            'number_request',
            'remaining_request'
        )

    def get_remaining_request(self, blockchair):
        return int(blockchair.total) - int(blockchair.number_request)
