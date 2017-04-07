from api.models.track import Track
from api.serializers.track import TrackSerializer
from api.models.follow import Follow

from rest_framework import filters, generics

from rest_framework.permissions import IsAuthenticated

class StreamList(generics.ListAPIView):
      serializer_class = TrackSerializer
      permission_classes = (IsAuthenticated,)

      def get_queryset(self):
          user = self.request.user
    
          # FIXME : optimize this request, avoid the map/in : join
          followed = map(lambda follow: follow.followed
                        ,Follow.objects.filter(owner_id=user))
            
          return (Track.objects.filter(owner_id__in=followed).order_by('-created_at'))
