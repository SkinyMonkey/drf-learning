from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from mixins import DateMixin

class Track(DateMixin):
    owner_id = models.ForeignKey(User)
#    playlist_id = models.ForeignKey(Playlist) # FIXME : complete at serialization?

    url_checksum = models.CharField(max_length=32) # , unique=True)

    name = models.CharField(max_length=64)
    provider = models.CharField(max_length=32)
    source_url = models.CharField(max_length=256)
#    image_url = models.CharField(max_length=256, default='') # FIXME : real default image

    # FIXME : add tags relationship?
    #         add likes?

    def __str__(self):
        return "%s" % self.name
