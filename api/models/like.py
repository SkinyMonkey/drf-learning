from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from mixins import DateMixin
from track import Track

#from rest_framework import generics
# FIXME : use genericForeignKey to use on comments, playlist and others?

class Like(DateMixin):
    owner_id = models.ForeignKey(User, related_name="liked")
    track_id = models.ForeignKey(Track, related_name="likes")


