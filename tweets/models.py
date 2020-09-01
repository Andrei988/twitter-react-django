from django.db import models

# Create your models here.

class Tweet(models.Model):
    # id = mdoels.AutoField(primary_key=True)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return str(self.id) + '\n' + self.content
