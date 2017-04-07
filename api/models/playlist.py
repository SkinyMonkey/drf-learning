from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from mixins import DateMixin

class Playlist(DateMixin):
    owner_id = models.ForeignKey(User)

    name = models.CharField(max_length=64)
    image_url = models.CharField(max_length=256, default='') # FIXME : real default image

    def __str__(self):
        return "%s" % self.name

# FIXME : remove related_name's ?
