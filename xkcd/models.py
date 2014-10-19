from django.contrib.auth.models import AbstractUser
from django.db import models


class Person(AbstractUser):
    pass

    def __unicode__(self):
        return unicode(self.username)


class Like(models.Model):
    comic_name = models.CharField(max_length=50)
    url = models.URLField()
    like_status = models.BooleanField(default=False)
    liked_by = models.ForeignKey(Person, related_name='likes')

    def __unicode__(self):
        return unicode(self.comic_name)
