# films/urls.py
from django.conf.urls import url, include

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers

from films.views import views, films_views, films_frontend_views, search_views
from films.api.v1 import api_views

from django_filters.views import FilterView
from films.filters import FilmFilter


urlpatterns = [ 
    # ws   
    url(r'^$', views.index, name='films_index'),
    url(r'^sync/(?P<room_name>[^/]+)/$', views.syncroom, name='syncroom'),
    url(r'^async/(?P<room_name>[^/]+)/$', views.asyncroom, name='asyncroom'),

    # backend visualize gap, len echart
    url(r'^chart/dash/list/$', films_views.DashBackendEChartsTemplate.as_view(), name='dash_backend'),
    url(r'^chart/gap/list/$', films_views.GapBackendEChartsTemplate.as_view(), name='gap_backend'),
    url(r'^chart/len/list/$', films_views.LenBackendEChartsTemplate.as_view(), name='len_backend'),
    
    # demo & test
    url(r'^chart/gap/', films_views.FilmGapView.as_view(), name='gap'),
    url(r'^chart/len/', films_views.FilmLenView.as_view(), name='len'),
    url(r'^dashboard/(?P<room_name>[^/]+)/$', films_views.dashboard, name='dashboard'),

    # frontend visualize
    url(r'^front/dash/list/$', films_frontend_views.DashIndex.as_view(), name='dash_front'),
    
    # Options Json for frontend views
    #url(r'options/dash/', films_frontend_views.DashView.as_view()),
    url(r'options/dash_yield/', films_frontend_views.DashViewYield.as_view()),
    url(r'options/dash_scatter/', films_frontend_views.DashViewScatter.as_view()),
    
    # cbv list
    url(r'^filmslist/$', films_frontend_views.FilmList.as_view(), name='film_list'),

    # search
    #url(r'^search/$', search_views.search, name='search'),
    url(r'^search/$', FilterView.as_view(
        filterset_class=FilmFilter,
        template_name='films/search.html', 
        paginate_by=5), name='search'),
    #url(r'^search/$', search_views.FilmSearch.as_view(), name='search')

]

apipattern = [
    # api
    url(r'^films/$', api_views.FilmView.as_view(), name='films_views_api'),
    url(r'^films/(?P<factory_id>[0-9a-f-]+)$', api_views.FilmViewDetail.as_view()),
    # api seq
    url(r'^filmseq/$', api_views.FilmSeqList.as_view(), name='films_seq_api'),
    url(r'^filmseq/(?P<pk>[0-9a-f-]+)$', api_views.FilmSeqDetail.as_view()),
    # api mix
    url(r'^filmsmixin/', api_views.FilmListMixin.as_view(), name='films_mixin_api'),
    # api statistical
    url(r'^static/', api_views.DashStatic.as_view(), name='film_statist_api'),
]

urlpatterns = format_suffix_patterns(urlpatterns + apipattern)
