from __future__ import unicode_literals

from django.utils import timezone
from django.db import models

class DateMixin(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super(DateMixin, self).save(*args, **kwargs)
