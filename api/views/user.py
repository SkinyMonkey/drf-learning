from django.contrib.auth.models import User, Group
from api.serializers.user import UserSerializer

from rest_framework import viewsets, filters, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('username', )


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


