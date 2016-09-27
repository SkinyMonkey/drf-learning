from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from rest_framework import generics
from django.utils import timezone

class DateMixin(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super(DateMixin, self).save(*args, **kwargs)

class Playlist(DateMixin):
    owner_id = models.ForeignKey(User)

    name = models.CharField(max_length=64)
    image_url = models.CharField(max_length=256, default='') # FIXME : real default image

    def __str__(self):
        return "%s" % self.name

class Track(DateMixin):
    owner_id = models.ForeignKey(User)
#    playlist_id = models.ForeignKey(Playlist)

    url_checksum = models.CharField(max_length=32) # , unique=True)

    name = models.CharField(max_length=64)
    provider = models.CharField(max_length=32)
    source_url = models.CharField(max_length=256)
#    image_url = models.CharField(max_length=256, default='') # FIXME : real default image

    # FIXME : add tags relationship?
    #         add likes?

    def __str__(self):
        return "%s" % self.name

# FIXME : remove related_name's ?

class Follow(DateMixin):
    owner_id = models.ForeignKey(User) # NOTE : was called followers, check if no pb
    followed = models.ForeignKey(User, related_name="followers")

# FIXME : use genericForeignKey to use on comments, playlist and others?
class Like(DateMixin):
    owner_id = models.ForeignKey(User, related_name="liked")
    track_id = models.ForeignKey(Track, related_name="likes")

class TrackPlaylist(DateMixin):
    owner_id = models.ForeignKey(User, related_name="owner")
    track_id = models.ForeignKey(Track, related_name="track")
    playlist_id = models.ForeignKey(Playlist, related_name="playlist")

# FIXME : use genericForeignKey to use on playlist too?
class Tag(DateMixin):
    owner_id = models.ForeignKey(User)
    track_id = models.ForeignKey(Track)

    name = models.CharField(max_length=32)
