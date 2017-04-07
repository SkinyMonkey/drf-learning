from django.contrib.auth.models import Group

from rest_framework import serializers

# FIXME : create a default playlist upon userCreation
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
