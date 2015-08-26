from django.conf.urls import url
from . import views

__author__ = 'agerasym'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'(?P<post_id>[0-9]+)/$', views.details, name='details'),
    url(r'(?P<post_id>[0-9]+)/created/$', views.created, name='created'),
    url(r'(?P<post_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'(?P<post_id>[0-9]+)/results/$', views.results, name='results'),
]
