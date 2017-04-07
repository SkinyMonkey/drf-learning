from api.models.track import Track
from api.serializers.track import TrackSerializer

from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class TrackView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows individual track to be viewed or edited.
    """
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

#    def get_queryset(self):
#        track_id = self.kwargs.get('pk')
#        print track_id
#        print Track.objects.get(id=track_id)
#
#        return Track.objects.get(id=track_id)

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
