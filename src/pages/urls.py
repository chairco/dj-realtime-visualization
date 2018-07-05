# pages/urls.py

from django.conf.urls import url

from . import views, backend_views


urlpatterns = [
    url(r'^backend_charts_list/$', backend_views.BackendEChartsTemplate.as_view(), name='backend_demo'),
    url(r'multiple/Page/', backend_views.PageDemoView.as_view(), name='page_demo'),
    url(r'multiple/NamedCharts/', backend_views.NamedChartsView.as_view(), name='namedcharts_demo'),
    url(r'^demo/temperature/', backend_views.TemperatureEChartsView.as_view()),
]
