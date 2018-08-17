#-*- coding: utf-8 -*-
from borax.fetch import fetch
from pyecharts import Bar, Pie

from films.models import FilmGap
from films.factory import ChartFactory


FACTORYGAP = ChartFactory()


@FACTORYGAP.collect('bar')
def create_bar_mix(num=200):
    decimal_places = 1
    film_datas = FilmGap.objects.all().order_by('id')[:num]
    ids = fetch(film_datas.values("id"), "id")
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

    return bar_mix


@FACTORYGAP.collect('pie')
def create_pie():
    pass






