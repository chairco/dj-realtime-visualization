# films/urls.py
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='films_index'),
    url(r'^async/(?P<room_name>[^/]+)/$', views.asyncroom, name='asyncroom'),
    url(r'^sync/(?P<room_name>[^/]+)/$', views.syncroom, name='syncroom'),
]
