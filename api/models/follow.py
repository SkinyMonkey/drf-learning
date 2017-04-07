from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from mixins import DateMixin

class Follow(DateMixin):
    owner_id = models.ForeignKey(User) # NOTE : was called followers, check if no pb
    followed = models.ForeignKey(User, related_name="followers")


