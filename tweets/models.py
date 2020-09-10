from datetime import datetime

from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Tweet(models.Model):
    id = models.AutoField(primary_key=True)
    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey('auth.User', null=False, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)
    likes = models.ManyToManyField(User, default=0, related_name='tweet_user', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        ordering = ['-id']

    @property
    def is_retweet(self):
        return self.parent is not None
