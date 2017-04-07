from api.models.like import Like
from api.serializers.like import LikeSerializer
from mq import MQViewSet

from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class LikeViewSet(MQViewSet):
    """
    API endpoint that relationships to be viewed or edited.
    """
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('created_at', 'updated_at', 'track_id', 'owner_id')

    def perform_create(self, serializer):
        serializer.save(owner_id=self.request.user)
        self.on_create(serializer)
