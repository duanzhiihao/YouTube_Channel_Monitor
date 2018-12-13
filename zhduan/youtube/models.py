from django.db import models

# Create your models here.
class despacito(models.Model):
    date = models.DateTimeField('current date')
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)