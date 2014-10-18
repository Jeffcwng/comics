import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models


class Person(AbstractUser):
    phone = models.CharField(max_length=12, null=True, blank=True, help_text="Format: 415-111-2222")
    today = datetime.date.today()

    def __unicode__(self):
        return unicode(self.username)


class Like(models.Model):
    comic_name = models.CharField(max_length=50)
    url = models.URLField()
    like_status = models.BooleanField(default=False)
    liked_by = models.ForeignKey(Person, related_name='likes')

    def __unicode__(self):
        return unicode(self.comic_name)
