from api.models.follow import Follow
from api.serializers.follow import FollowSerializer
from mq import MQViewSet

from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class FollowViewSet(MQViewSet):
    """
    API endpoint that relationships to be viewed or edited.
    """
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('created_at', 'updated_at', 'followed', 'owner_id')

    def perform_create(self, serializer):
        serializer.save(owner_id=self.request.user)
        self.on_create(serializer)


