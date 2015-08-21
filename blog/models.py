from django.db import models

# Create your models here.


class Post(models.Model):

    body = None
    created = None
    user = None

    class Meta:
        db_table = 'blog_posts'
