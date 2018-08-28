# films/films_fronted_views.py
import datetime

from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.utils import timezone

from django_echarts.views.frontend import EChartsFrontView

from films.load_dashdata import FACTORYDASH
from films.models import Film


class DashIndex(TemplateView):
    template_name = 'films/frontend_dashcharts.html'


class DashViewStatic(ListView):
    template_name = 'films/frontend_dashcharts.html'
    context_object_name = 'rs232_time'
    paginate_by = 1

    def get_queryset(self):
        latest_film = Film.objects.order_by('-rs232_time')[0]
        last_time = latest_film.rs232_time - datetime.timedelta(hours=1)
        return Film.objects.filter(rs232_time__gte=last_time).count()


class DashView(EChartsFrontView):
    def get_echarts_instance(self, **kwargs):
        return FACTORYDASH.create('dash', hours=1)


class DashViewYield(EChartsFrontView):
    def get_echarts_instance(self, **kwargs):
        return FACTORYDASH.create('dash_yield', hours=1)


class DashViewScatter(EChartsFrontView):
    def get_echarts_instance(self, **kwargs):
        return FACTORYDASH.create('dash_scatter', hours=1)


class FilmList(ListView):
    template_name = 'films/films_list.htm'
    model = Film
    paginate_by = 6
