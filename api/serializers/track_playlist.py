from api.models.track_playlist import TrackPlaylist

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

class TrackPlaylistSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = TrackPlaylist
        fields = ('id', 'created_at', 'updated_at', 'owner_id', 'track_id', 'playlist_id')
        validators = [
                UniqueTogetherValidator(
                    queryset=TrackPlaylist.objects.all(),
                    fields=('track_id', 'playlist_id'),
                    message='TRACK_ALREADY_IN_PLAYLIST',)
                ]
