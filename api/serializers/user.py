from django.contrib.auth.models import User

from rest_framework import serializers

# FIXME : add password confirmation
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups', 'password')
        extra_kwargs = {'password': {'write_only': True}
                       ,'email': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
