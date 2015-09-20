import datetime
from django.utils import timezone
from django.test import TestCase
from ..models import Post
from django.core.urlresolvers import reverse

__author__ = 'agerasym'


def create_post(body, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Post.objects.create(body=body, created=time)


class PostMethodTests(TestCase):

    def test_was_published_recently_old_posts(self):
        fut_date = timezone.now() + datetime.timedelta(days=30)
        fut_post = Post(created=fut_date)
        self.assertEqual(fut_post.was_published_recently(), False)

    def test_was_published_recently_recent_post(self):
        fut_date = timezone.now() - datetime.timedelta(hours=1)
        fut_post = Post(created=fut_date)
        self.assertEqual(fut_post.was_published_recently(), True)


class PostViewTest(TestCase):
    def test_index_view_with_no_posts(self):
        Post.objects.all().delete()
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No posts are available')

    def test_index_view_with_past_posts(self):
        Post.objects.all().delete()
        create_post('Past post', days=-4)
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['latest_post'],
            ['<Post: Post object>']
        )

    def test_index_view_with_future_posts(self):
        Post.objects.all().delete()
        create_post('Past post', days=30)
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['latest_post'], [])

    def test_index_view_with_past_and_future_posts(self):
        Post.objects.all().delete()
        create_post('Past post', days=-4)
        create_post('Past post', days=4)
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['latest_post'],
            ['<Post: Post object>']
        )

    def test_index_view_with_two_past_posts(self):
        Post.objects.all().delete()
        create_post('Past post', days=-4)
        create_post('Past post', days=-15)
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['latest_post'],
            ['<Post: Post object>', '<Post: Post object>']
        )










