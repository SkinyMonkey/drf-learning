from django.contrib.auth.models import User, Group
from api.models import Playlist, Track, Follow, Like, TrackPlaylist
from rest_framework import serializers

from rest_framework.validators import UniqueTogetherValidator

import shortuuid
import requests
import re

PROVIDERS = ["youtube", "soundcloud"]
PROVIDERS_REGEX = re.compile(".*(%s).*" % '|'.join(PROVIDERS)) 
YOUTUBE_CHECK_URL = "https://www.youtube.com/oembed?format=json&url="

# FIXME : Will disappear as use API directly?
TITLE_REGEX = re.compile("<title.*?>(.+?)</title>")

#SC_TITLE_REGEX = re.compile('<meta property="og:title" content="(.*?)">')

class DateSerializer:
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

# FIXME : no editable field
class TrackSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(read_only=True)

    provider = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
#    image_url = serializers.URLField(read_only=True)

    # FIXME : this should not be editable
#    source_url = serializers.URLField(validators=[track_validations])

    class Meta:
        model = Track 
        fields = ('id', 'source_url', 'name', 'provider', 'created_at', 'updated_at', 'owner_id')

    def extract_track_info(self, validated_data):
        source_url = validated_data['source_url']
    
        validated_data['provider'] = self.provider
    
        answer = self.get_page(source_url, self.provider)
    
        if (answer.headers['content-type'] == 'application/json'):
            answer = answer.json()
            validated_data['name'] = answer['title'] or answer['name']
        else:
            validated_data['name'] = TITLE_REGEX.match(answer.text).group(1)
    
        return validated_data
 
    def create(self, validated_data):
        validated_data = self.extract_track_info(validated_data)

        source_url = str(validated_data['source_url'])

        validated_data['url_checksum'] = self.uuid;

        return super(TrackSerializer, self).create(validated_data)

    # FIXME : use youtube API
    def get_page(self, source_url, provider):
        if provider == "youtube":
            answer = requests.get(YOUTUBE_CHECK_URL + source_url)
    
        elif provider == "soundcloud":
            answer = requests.get(source_url)
    
        return answer
   
    # FIXME : make it stronger at the Regex level
    def valid_provider(self, source_url):
        provider = PROVIDERS_REGEX.match(source_url)
        if provider == None:
            raise serializers.ValidationError("INVALID_PROVIDER")
            #raise serializers.ValidationError("Invalid provider, must be from %s" % ', '.join(PROVIDERS))
        return provider.group(1)
    
    def track_exists(self):
        print "track_exists"
    
        answer = self.get_page(self.source_url, self.provider)
    
        if answer.status_code != 200:
           raise serializers.ValidationError({"non_field_errors": "UNEXISTING_VIDEO_SOURCE"})
    
#    def unique_track(self, uuid):
#        print "unique_track"
#    
#        row = Track.objects.filter(url_checksum=uuid)
#    
#        if row.count() > 0:
#           raise serializers.ValidationError("TRACK_ALREADY_REGISTERED")
 
    def unique_track_in_playlist(self, playlist_id):
        print "unique_track_in_playlist"

        if not self.track:
           return

        tracks = TrackPlaylist.objects.filter(track_id=self.track.id
                                             ,playlist_id=playlist_id)

        if tracks.count() != 0:
            raise serializers.ValidationError({"non_field_errors": "TRACK_ALREADY_REGISTERED"})
    
    def validate(self, payload):
        self.source_url = payload['source_url']
 
        self.provider = self.valid_provider(self.source_url)

        self.uuid = shortuuid.uuid(name=str(self.source_url))
    
        tracks = Track.objects.filter(url_checksum=self.uuid)

        if tracks.count() == 0:
            self.track = None
        else:
            self.track = tracks[0]

#        self.unique_track_in_playlist(self.uuid, playlist_id)
#        self.track_exists(source_url, self.provider)

        return payload

# FIXME : CurrentUserDefault : all right? will it default all the time
#         taking the current user as default even if we don't own it?
#         try by retrieving a track that is not owned by the requesting account

# FIXME : only name and image_url are editable
class PlaylistSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    image_url = serializers.URLField(required=False)

    class Meta:
        model = Playlist
        fields = ('id', 'name', 'created_at', 'updated_at', 'image_url', 'owner_id')
        validators = [
                UniqueTogetherValidator(
                    queryset=Playlist.objects.all(),
                    fields=('name', 'owner_id'),
                    message='PLAYLIST_ALREADY_EXISTS',)
                ]

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

# FIXME : create a default playlist upon userCreation
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
