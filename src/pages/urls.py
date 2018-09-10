# pages/urls.py
from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib.auth.decorators import login_required, permission_required

from pages.views import views, backend_views, api


urlpatterns = [
    url(r'^backend_charts_list/$', backend_views.BackendEChartsTemplate.as_view(), name='backend_demo'),
    url(r'^multiple/Page/', backend_views.PageDemoView.as_view(), name='page_demo'),
    url(r'^multiple/NamedCharts/', backend_views.NamedChartsView.as_view(), name='namedcharts_demo'),
    url(r'^demo/temperature/', backend_views.TemperatureEChartsView.as_view()),

    # api
    url(r'^filmgaps_class/$', api.FilmList.as_view()),    
    url(r'^filmgaps/$', api.film_list),

    # blog(index's information)
    url(r'^(?P<pk>\d+)/$', views.BlogDetail.as_view(), name='blog_detail'),
    url(r'^add/$', login_required(views.BlogCreateView.as_view()), name='blog_add'),
    url(r'^(?P<pk>\d+)/edit/$', views.BlogUpdateView.as_view(), name='blog_edit'),
]


urlpatterns = format_suffix_patterns(urlpatterns)