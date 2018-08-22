# films/films_views.py
from borax.fetch import fetch

from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.db.models import Count
from django.core.serializers.json import DjangoJSONEncoder

from django_echarts.views.backend import EChartsBackendView

from pyecharts import Line, Pie, Page, Bar, Boxplot

from films.models import FilmGap, FilmLen, FilmType, Film, Message
from films.load_gapdata import FACTORYGAP
from films.load_lendata import FACTORYLEN
from films.load_dashdata import FACTORYDASH

import json


def dashboard(request, room_name):
    """
    TODO(demo dashboard)
    """
    chat_messages = Message.objects.filter(group_name=room_name).order_by("created")[:100]
    return render(request, 'films/dashboard.html', {
        'chat_messages': chat_messages,
        'room_name_json': mark_safe(json.dumps(room_name))
    })


class FilmGapView(EChartsBackendView):
    echarts_instance_name = 'page'
    template_name = 'films/films.html'

    def get_echarts_instance(self, *args, **kwargs):
        decimal_places = 1
        film_datas = FilmGap.objects.all().order_by('-id')[:200]
        ids = fetch(film_datas.values("id"), "id")
        ids.reverse()

        # bar
        bar_mix = Bar("間距", page_title='(BarMix)', width='100%')
        for i in range(0, 6):
            bar_data = fetch(film_datas.values(f"gap{i}"), f"gap{i}")
            bar_mix.add(
                f"gap{i}",
                ids,
                list(map(lambda x:round(x, decimal_places), bar_data)),
                is_stack=True,
                is_datazoom_show=True
            )
        page = Page.from_charts(bar_mix)
        return page


class FilmLenView(EChartsBackendView):
    echarts_instance_name = 'page'
    template_name = 'films/films.html'
    len_map = ['pink', 'orange', 'yellow', 'green', 'blue']
    
    def get_echarts_instance(self, *args, **kwargs):
        decimal_places = 1
        film_datas = FilmLen.objects.all().order_by('id')[:200]
        ids = fetch(film_datas.values("id"), "id")

        # bar
        bar_mix = Bar("Film 長度", page_title='(BarMix)', width='100%')
        for i in range(0, 5):
            bar_data = fetch(film_datas.values(f"{self.len_map[i]}"), f"{self.len_map[i]}")
            bar_mix.add(
                f"{self.len_map[i]}",
                ids,
                list(map(lambda x:round(x, decimal_places), bar_data)),
                is_stack=True,
                is_datazoom_show=True
            )

        page = Page.from_charts(bar_mix)
        return page


class DashBackendEChartsTemplate(EChartsBackendView):
    template_name = 'films/backend_charts.html'

    def get_echarts_instance(self, *args, **kwargs):
        name = self.request.GET.get('name', 'dash')
        return FACTORYDASH.create(name, hours=4)

    def get_template_names(self):
        return super().get_template_names()


class GapBackendEChartsTemplate(EChartsBackendView):
    template_name = 'films/backend_charts.html'

    def get_echarts_instance(self, *args, **kwargs):
        name = self.request.GET.get('name', 'bar')
        if name == 'bar':
            return FACTORYGAP.create(name, num=200)
        return FACTORYGAP.create(name)

    def get_template_names(self):
        return super().get_template_names()


class LenBackendEChartsTemplate(EChartsBackendView):
    template_name = 'films/backend_charts.html'

    def get_echarts_instance(self, *args, **kwargs):
        name = self.request.GET.get('name', 'bar')
        if name == 'bar':
            return FACTORYLEN.create(name, num=200)
        return FACTORYLEN.create(name)

    def get_template_names(self):
        return super().get_template_names()

