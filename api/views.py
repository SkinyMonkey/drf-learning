from django.contrib.auth.models import User, Group
from api.models import Playlist, Track, Follow, Like, TrackPlaylist
from rest_framework import viewsets, filters, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from api.serializers import UserSerializer, GroupSerializer, PlaylistSerializer, TrackSerializer, FollowSerializer, LikeSerializer

# Swagger view
# FIXME : move to separate file
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import response, schemas

# FIXME : move to separate file
@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='Whyd API')
    return response.Response(generator.get_schema(request=request))

class MQViewSet(viewsets.ModelViewSet):
    def __init__(self, *args, **kwargs):
        super(MQViewSet, self).__init__(*args, **kwargs)
        model_name = self.__class__.__name__.lower()
        self.post_topic_key = "model." + model_name + ".post";
        self.update_topic_key = "model." + model_name + ".update";
        self.delete_topic_key = "model." + model_name + ".delete";

    def on_create(self, serializer):
        print "SERIALIZER: %s" % serializer.data
        print self.post_topic_key

#        channel.basic_publish(exchange='whyd',
#                              routing_key=self.post_topic_key,
#                              body=serializer.data)

    def on_update(self, serializer):
        print "SERIALIZER: %s" % serializer.data
        print self.update_topic_key

#        channel.basic_publish(exchange='whyd',
#                              routing_key=self.update_topic_key,
#                              body=serializer.data)

    def on_destroy(self, instance):
        print "DELETE INSTANCE: %s" % instance.id
        print self.delete_topic_key

#        channel.basic_publish(exchange='whyd',
#                              routing_key=self.delete_topic_key,
#                              body=serializer.data)
    
    def perform_create(self, serializer):
        super(MQViewSet, self).perform_create(serializer)
        self.on_create(serializer)

    def perform_update(self, serializer):
        super(MQViewSet, self).perform_update(serializer)
        self.on_update(serializer)

    def perform_destroy(self, serializer):
        super(MQViewSet, self).perform_destroy(serializer)
        self.on_destroy(serializer)

# FIXME : break to separate files

# FIXME : what if user not logged?
class PlaylistViewSet(MQViewSet):
    """
    API endpoint that allows playlists to be viewed or edited.
    """
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('name', 'created_at', 'updated_at', 'owner_id')
    search_fields = ('name',)

    def perform_create(self, serializer):
        serializer.save(owner_id=self.request.user)
        self.on_create(serializer)

class ListTrackView(generics.ListAPIView):
    """
    API endpoint that allows tracks to be viewed or searched.
    """
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('name', 'created_at', 'updated_at', 'owner_id', 'source_url')
    search_fields = ('name',)

#    def perform_create(self, serializer):
#        serializer.save(owner_id=self.request.user)
#        self.on_create(serializer)

class TrackView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows individual track to be viewed or edited.
    """
    queryset = Track.objects.all()
    serializer_class = TrackSerializer

#    def get_queryset(self):
#        track_id = self.kwargs.get('pk')
#        print track_id
#        print Track.objects.get(id=track_id)
#
#        return Track.objects.get(id=track_id)

class FollowViewSet(MQViewSet):
    """
    API endpoint that relationships to be viewed or edited.
    """
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('created_at', 'updated_at', 'followed', 'owner_id')

    def perform_create(self, serializer):
        serializer.save(owner_id=self.request.user)
        self.on_create(serializer)

class LikeViewSet(MQViewSet):
    """
    API endpoint that relationships to be viewed or edited.
    """
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('created_at', 'updated_at', 'track_id', 'owner_id')

    def perform_create(self, serializer):
        serializer.save(owner_id=self.request.user)
        self.on_create(serializer)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('username', )

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAdminUser,)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def current_user(request):
    serializer = UserSerializer(request.user, context={'request': request})
    return Response(serializer.data)

"""
 # FIXME : finish
class CurrentUserDetail(generics.RetrieveAPIView):
      serializer_class = UserSerializer
      permission_classes = (IsAuthenticated,)

      def get_queryset(self):
          serializer = UserSerializer(request.user, context={'request': request})
          return Response(serializer.data)
"""

class StreamList(generics.ListAPIView):
      serializer_class = TrackSerializer
      permission_classes = (IsAuthenticated,)

      def get_queryset(self):
          user = self.request.user
    
          # FIXME : optimize this request, avoid the map/in
          followed = map(lambda follow: follow.followed
                        ,Follow.objects.filter(owner_id=user))
            
          return (Track.objects.filter(owner_id__in=followed).order_by('-created_at'))

class DeletePlaylistTrackView(generics.DestroyAPIView):
    """
    """
    serializer_class = TrackSerializer
    permission_classes = (IsAuthenticated,)

    def perform_destroy(self, serializer):
        playlist_id = self.kwargs['playlist_id']
        track_id = self.kwargs['track_id']

        # FIXME : try/catch?
        return TrackPlaylist.objects.filter(track_id=track_id, playlist_id=playlist_id).delete()

class ListPlaylistTracksView(generics.ListCreateAPIView):
    """
    API endpoint that allows tracks of a playlist to be created and viewed
    
    /playlists/{pk}/tracks
    """
    serializer_class = TrackSerializer

    def get_queryset(self):
        playlist_id = self.kwargs.get('playlist_id')

        # FIXME : optimize this request, avoid the map/in
        playlist_tracks = map(lambda playlist_track: playlist_track.track_id.id
                             ,TrackPlaylist.objects.filter(playlist_id=playlist_id));

        return Track.objects.filter(id__in=playlist_tracks).order_by('-created_at')

    def perform_create(self, serializer):
        playlist_id = self.kwargs['playlist_id']

        # FIXME : replace with uniquetogethervaldator?
        serializer.unique_track_in_playlist(playlist_id)

        if not serializer.track:
            serializer.track_exists()
            track = serializer.save(owner_id=self.request.user)
        else:
            track = serializer.track

        playlist = Playlist.objects.get(id=playlist_id)
        
        TrackPlaylist.objects.create(playlist_id=playlist, track_id=track, owner_id=self.request.user)
        #self.on_create(serializer)
