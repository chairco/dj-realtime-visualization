# films/films_views.py
from borax.fetch import fetch

from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.db.models import Count
from django.core.serializers.json import DjangoJSONEncoder

from django_echarts.views.backend import EChartsBackendView

from pyecharts import Line, Pie, Page, Bar, Boxplot

from films.models import FilmGap, FilmLen, FilmType, Film
from films.load_gapdata import FACTORYGAP
from films.load_lendata import FACTORYLEN

import json


class FilmGapView(EChartsBackendView):
    echarts_instance_name = 'page'
    template_name = 'films/films_gap.html'

    def get_echarts_instance(self, *args, **kwargs):
        decimal_places = 1
        film_datas = FilmGap.objects.all().order_by('id')[:200]
        ids = fetch(film_datas.values("id"), "id")

        # bar mix
        bar_mix = Bar("Gap 長度", page_title='(BarMix)', width='100%')
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
    template_name = 'films/films_gap.html'
    len_map = ['pink', 'orange', 'yellow', 'green', 'blue']
    
    def get_echarts_instance(self, *args, **kwargs):
        decimal_places = 1
        film_datas = FilmLen.objects.all().order_by('id')[:200]
        ids = fetch(film_datas.values("id"), "id")

        # bar mix
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


class GapBackendEChartsTemplate(EChartsBackendView):
    template_name = 'films/backend_charts.html'

    def get_echarts_instance(self, *args, **kwargs):
        name = self.request.GET.get('name', 'bar')
        if name == 'bar':
            return FACTORYGAP.create(name, num=200)
        elif name == 'mix':
            return FACTORYGAP.create(name, hours=4)
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



