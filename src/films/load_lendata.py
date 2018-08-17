#-*- coding: utf-8 -*-
from borax.fetch import fetch
from pyecharts import Bar, Pie

from films.models import FilmLen
from films.factory import ChartFactory

FACTORYLEN = ChartFactory()


@FACTORYLEN.collect('bar')
def create_bar_mix(num=200):
    len_map = ['pink', 'orange', 'yellow', 'green', 'blue']
    decimal_places = 1
    film_datas = FilmLen.objects.all().order_by('id')[:num]
    ids = fetch(film_datas.values("id"), "id")

    bar_mix = Bar("Film 長度", page_title='(BarMix)', width='100%')
    for i in range(0, 5):
        bar_data = fetch(film_datas.values(f"{len_map[i]}"), f"{len_map[i]}")
        bar_mix.add(
            f"{len_map[i]}",
            ids,
            list(map(lambda x:round(x, decimal_places), bar_data)),
            is_stack=True,
            is_datazoom_show=True
        )

    return bar_mix


@FACTORYLEN.collect('pie')
def create_pie():
    pass