from django.conf.urls import url
from . import views

__author__ = 'agerasym'


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'(?P<pk>[0-9]+)/$', views.DetailsView.as_view(),
        name='details'),
    url(r'(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(),
        name='results'),
    url(r'(?P<post_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'(?P<post_id>[0-9]+)/created/$', views.created, name='created'),
]

