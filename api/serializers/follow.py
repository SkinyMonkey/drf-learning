from api.models.follow import Follow

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

class FollowSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Follow
        fields = ('id', 'created_at', 'updated_at', 'owner_id', 'followed')
        validators = [
                UniqueTogetherValidator(
                    queryset=Follow.objects.all(),
                    fields=('followed', 'owner_id'),
                    message='USER_ALREADY_FOLLOWING',)
                ]

    def validate_followed(self, value):
        user = self.context['request'].user
        if (user.id == value.id):
            raise serializers.ValidationError("CANT_FOLLOW_SELF")
        return value
