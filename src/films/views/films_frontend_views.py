# films/films_fronted_views.py
from django.views.generic.base import TemplateView
from django_echarts.views.frontend import EChartsFrontView

from films.load_dashdata import FACTORYDASH


class DashIndex(TemplateView):
    template_name = 'films/frontend_dashcharts.html'


class SimpleDashView(EChartsFrontView):
    def get_echarts_instance(self, **kwargs):
        return FACTORYDASH.create('dash', hours=1)