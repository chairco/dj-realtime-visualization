# films/urls.py
from django.conf.urls import url, include

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers

from films.views import views, films_views
from films.api.v1 import api_views


urlpatterns = [ 
    # ws   
    url(r'^$', views.index, name='films_index'),
    url(r'^sync/(?P<room_name>[^/]+)/$', views.syncroom, name='syncroom'),
    url(r'^async/(?P<room_name>[^/]+)/$', views.asyncroom, name='asyncroom'),
    url(r'^dashboard/(?P<room_name>[^/]+)/$', views.dashboard, name='dashboard'),

    # visualize gap echart
    url(r'^chart/gap/list/$', films_views.GapBackendEChartsTemplate.as_view(), name='gap_backend'),
    url(r'^chart/gap/bar_mix/', films_views.FilmGapView.as_view(), name='gap'),
    
    # visualize len echart
    url(r'^chart/len/list/$', films_views.LenBackendEChartsTemplate.as_view(), name='len_backend'),
    url(r'^chart/len/bar_mix/', films_views.FilmLenView.as_view(), name='len'),
]

apipattern = [
    # rest api
    url(r'^films/', api_views.FilmView.as_view(), name='films_list'),
    url(r'^filmsmixin/', api_views.FilmListMixin.as_view(), name='films_mixin'),
    url(r'^filmseq/', api_views.FilmSeqMixin.as_view(), name='films_seq_mixin'),
]

urlpatterns = format_suffix_patterns(urlpatterns + apipattern)
