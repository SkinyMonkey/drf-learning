from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from mixins import DateMixin
from track import Track

# FIXME : use genericForeignKey to use on playlist too?
class Tag(DateMixin):
    owner_id = models.ForeignKey(User)
    track_id = models.ForeignKey(Track)

    name = models.CharField(max_length=32)
