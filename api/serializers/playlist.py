from api.models.playlist import Playlist

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

# FIXME : only name and image_url are editable
class PlaylistSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    image_url = serializers.URLField(required=False)

    # FIXME : editable =True

    class Meta:
        model = Playlist
        fields = ('id', 'name', 'created_at', 'updated_at', 'image_url', 'owner_id')
        validators = [
                UniqueTogetherValidator(
                    queryset=Playlist.objects.all(),
                    fields=('name', 'owner_id'),
                    message='PLAYLIST_ALREADY_EXISTS',)
                ]
