from django.db import models


# Create your models here.


class Post(models.Model):
    body = models.CharField(max_length=15)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User', related_name='post')

    class Meta:
        db_table = 'blog_posts'


class Choices(models.Model):
    choice_text = models.TextField(max_length=200)
    votes = models.IntegerField(default=0)
    post = models.ForeignKey(Post)

    class Meta:
        db_table = 'blog_choices'

