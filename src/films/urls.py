# films/urls.py
from django.conf.urls import url, include

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers

from films.views import views, films_views
from films.api.v1 import api_views


urlpatterns = [    
    url(r'^$', views.index, name='films_index'),
    url(r'^dashboard/(?P<room_name>[^/]+)/$', views.dashboard, name='dashboard'),
    url(r'^sync/(?P<room_name>[^/]+)/$', views.syncroom, name='syncroom'),
    url(r'^async/(?P<room_name>[^/]+)/$', views.asyncroom, name='asyncroom'),
]

apipattern = [
    # rest api
    url(r'^films/', api_views.FilmView.as_view(), name='films_list'),
    url(r'^filmsmixin/', api_views.FilmList.as_view(), name='films_mixin'),
]

urlpatterns = format_suffix_patterns(urlpatterns + apipattern)
