from django.contrib.auth.models import Group
from api.serializers.group import GroupSerializer

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
