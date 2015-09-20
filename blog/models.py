from django.utils import timezone
import datetime
from django.db import models


# Create your models here.
_app_label = 'blog'


class Post(models.Model):
    body = models.CharField(max_length=15)
    created = models.DateTimeField()
    user = models.ForeignKey('auth.User', related_name='post')

    class Meta:
        db_table = 'blog_posts'
        app_label = _app_label

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.created <= now


class Choices(models.Model):
    choice_text = models.TextField(max_length=200)
    votes = models.IntegerField(default=0)
    post = models.ForeignKey(Post)

    class Meta:
        db_table = 'blog_choices'
        app_label = _app_label
