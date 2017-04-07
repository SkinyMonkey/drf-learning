from api.models.playlist import Playlist
from api.models.track import Track
from api.models.track_playlist import TrackPlaylist
from api.serializers.track import TrackSerializer
from api.serializers.playlist import PlaylistSerializer
from api.serializers.track_playlist import TrackPlaylistSerializer
from mq import MQViewSet

from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

# FIXME : what if user not logged?
class PlaylistViewSet(MQViewSet):
    """
    API endpoint that allows playlists to be viewed or edited.
    """
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('name', 'created_at', 'updated_at', 'owner_id')
    search_fields = ('name',)

    def perform_create(self, serializer):
        serializer.save(owner_id=self.request.user)
        self.on_create(serializer)

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
