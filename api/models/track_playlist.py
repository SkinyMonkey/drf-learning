from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from mixins import DateMixin
from track import Track
from playlist import Playlist

class TrackPlaylist(DateMixin):
    owner_id = models.ForeignKey(User, related_name="owner")
    track_id = models.ForeignKey(Track, related_name="track")
    playlist_id = models.ForeignKey(Playlist, related_name="playlist")
