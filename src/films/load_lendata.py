#-*- coding: utf-8 -*-
from borax.fetch import fetch
from pyecharts import Bar, Pie

from films.models import FilmLen
from films.factory import ChartFactory


FACTORYLEN = ChartFactory()


@FACTORYLEN.collect('bar')
def create_bar_mix(num):
    len_map = ['pink', 'orange', 'yellow', 'green', 'blue']
    decimal_places = 1
    film_datas = FilmLen.objects.all().order_by('-id')[:num]
    ids = fetch(film_datas.values("id"), "id")
    #ids = [ str(f.film) for f in film_datas]
    ids.reverse()
    bar_mix = Bar("膠條長度", page_title='(BarMix)', width='100%')
    for i in range(0, 5):
        bar_data = fetch(film_datas.values(f"{len_map[i]}"), f"{len_map[i]}")
        bar_data.reverse()
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
    pie = Pie('膠條良率', "數據", title_pos='center', width='100%')
    pie.add("", ["紅", ""], [25, 75], center=[10, 30], radius=[18, 24],
            label_pos='center', is_label_show=True, label_text_color=None, )
    pie.add("", ["橘", ""], [24, 76], center=[30, 30], radius=[18, 24],
            label_pos='center', is_label_show=True, label_text_color=None, legend_pos='left')
    pie.add("", ["黃", ""], [14, 86], center=[50, 30], radius=[18, 24],
            label_pos='center', is_label_show=True, label_text_color=None)
    pie.add("", ["綠", ""], [11, 89], center=[70, 30], radius=[18, 24],
            label_pos='center', is_label_show=True, label_text_color=None)
    pie.add("", ["藍", ""], [27, 73], center=[90, 30], radius=[18, 24],
            label_pos='center', is_label_show=True, label_text_color=None, is_legend_show=True, legend_top="center")
    pie.renderer = 'svg'
    return pie


