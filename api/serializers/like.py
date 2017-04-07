from api.models.like import Like

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

class LikeSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Like
        fields = ('id', 'created_at', 'updated_at', 'owner_id', 'track_id')
        validators = [
                UniqueTogetherValidator(
                    queryset=Like.objects.all(),
                    fields=('track_id', 'owner_id'),
                    message='USER_ALREADY_LIKED',)
                ]


