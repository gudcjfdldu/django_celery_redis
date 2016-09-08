from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class VisitInfo(models.Model):
    hits = models.IntegerField(default=0)

    def hit_update(self):
        self.hits = self.hits + 1
        self.save()


    def get_hits(self):
        return self.hits

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    email = models.EmailField(blank=True, default='', null=True)
    visitinfo = models.OneToOneField(VisitInfo)

    def __unicode__(self):
        return self.user.username


    def visit(self):
        self.visitinfo.hit_update()
        self.save()


