# films/urls.py
from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns

from . import views, films_views, api_views


urlpatterns = [
    url(r'^$', views.index, name='films_index'),
    
    url(r'^async/(?P<room_name>[^/]+)/$', views.asyncroom, name='asyncroom'),
    url(r'^sync/(?P<room_name>[^/]+)/$', views.syncroom, name='syncroom'),
    
    url(r'^dashboard/(?P<room_name>[^/]+)/$', views.dashboard, name='dashboard'),
    
    url(r'^gap/', films_views.FilmGapView.as_view(), name='film_gap'),

    # rest api
    url(r'^filmsmixin/', api_views.FilmList.as_view(), name='films_mixin'),
    url(r'^films/', api_views.FilmView.as_view(), name='films_list'),
    url(r'^filmsgap/', api_views.FilmGapView.as_view(), name='film_gap_list'),
    url(r'^filmslen/', api_views.FilmLenView.as_view(), name='film_len_list'),
]


urlpatterns = format_suffix_patterns(urlpatterns)