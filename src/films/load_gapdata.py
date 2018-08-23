#-*- coding: utf-8 -*-
import datetime
import itertools

from borax.fetch import fetch
from pyecharts import Bar, Pie, Line, Grid, Style

from films.models import FilmGap, Film
from films.factory import ChartFactory

from django.db.models import Count, Q

from collections import OrderedDict

FACTORYGAP = ChartFactory()


@FACTORYGAP.collect('bar')
def create_bar_mix(num):
    decimal_places = 2
    film_datas = FilmGap.objects.all().order_by('-id')[:num]
    ids = fetch(film_datas.values("id"), "id")
    ids.reverse()
    bar_mix = Bar("貼合間距", page_title='(BarMix)', width='100%')
    for i in range(0, 6):
        bar_data = fetch(film_datas.values(f"gap{i}"), f"gap{i}")
        bar_data.reverse() # reverse data, change order
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
    film_datas = FilmGap.objects.all()
    spec = {
        'gap0': [1, 1.5], 'gap1': [1.8, 2.3], 'gap2': [1.8, 2.3], 
        'gap3': [1.8, 2.3], 'gap4': [1.8, 2.3], 'gap5': [1, 1.5]
    }
    pie = Pie('貼合良率', "數據", title_pos='center', width='100%')
    style = Style()
    pie_style = style.add(
        label_pos="center",
        is_label_show=True,
        label_text_color=None
    )
    static = {}
    for i in range(0, 6):
        gap = f"gap{i}"
        lower, upper = spec.get(gap)
        if i == 0:
            fail_count = FilmGap.objects \
                .annotate(num=Count(gap)) \
                .filter(Q(gap0__gte=upper)|Q(gap0__lte=lower))
            center = [20, 30]
        elif i == 1:
            fail_count = FilmGap.objects \
                .annotate(num=Count(gap)) \
                .filter(Q(gap1__gte=upper)|Q(gap1__lte=lower))
            center = [40, 30]
        elif i == 2:
            fail_count = FilmGap.objects \
                .annotate(num=Count(gap)) \
                .filter(Q(gap2__gte=upper)|Q(gap2__lte=lower))
            center = [60, 30]
        elif i == 3:
            fail_count = FilmGap.objects \
                .annotate(num=Count(gap)) \
                .filter(Q(gap3__gte=upper)|Q(gap3__lte=lower))
            center = [80, 30]
        elif i == 4:
            fail_count = FilmGap.objects \
                .annotate(num=Count(gap)) \
                .filter(Q(gap4__gte=upper)|Q(gap4__lte=lower))
            center = [20, 70]
        elif i == 5:
            fail_count = FilmGap.objects \
                .annotate(num=Count(gap)) \
                .filter(Q(gap5__gte=upper)|Q(gap5__lte=lower))
            center=[40, 70]
        
        static.setdefault(gap, len(fail_count))
        f = (static.get(gap) / len(film_datas)) * 100
        p = 100 - f
        ration = [f"{f:.1f}", f"{p:.1f}"]
        
        if i == 1:
            pie.add(gap, [gap, ""], ration, center=center, radius=[20, 26],
                    **pie_style, legend_pos='left')
        elif i == 5:
            pie.add(gap, [gap, ""], ration, center=center, radius=[20, 26],
                    **pie_style, is_legend_show=True, legend_top="center")
        else:
            pie.add(gap, [gap, ""], ration, center=center, radius=[20, 26],
                    **pie_style) 
    pie.renderer = 'svg'
    return pie


@FACTORYGAP.collect('dash')
def create_mix(hours):
    """
    create bar+line to show yield rate in the time interval
    """
    latest_film = Film.objects.order_by('-rs232_time')[0]
    last_time = latest_film.rs232_time - datetime.timedelta(hours=hours) #latest 24h
    film_datas = Film.objects.filter(rs232_time__gte=last_time)
    # count the yield of mins
    grouped = itertools.groupby(film_datas, lambda f: f.rs232_time.strftime("%Y-%m-%d %H:%M"))
    data_records = {day: len(list(g)) for day, g in grouped}
    # get all time interval 
    data_gaps = {d: 0 for d in gen_dates(last_time, latest_film.rs232_time)}
    # combine missing time
    data_all = {**data_gaps, **data_records}
    # sort data by key
    data_filter = OrderedDict(sorted(data_all.items(), key=lambda t: t[0]))

    attr = list(data_filter.keys())
    cam0 = list(data_filter.values())
    
    bar = Bar("產能柱狀圖", height=720)
    bar.add("cam0", attr, cam0, is_stack=True, is_datazoom_show=True, datazoom_xaxis_index=[0, 1],)

    line = Line("產能折線圖", title_top="50%")
    line.add(
        "cam0", attr, cam0,
        mark_point=["max", "min"],
        mark_line=["average"],
        legend_top="50%",
        is_datazoom_show=True,
    )

    grid = Grid(width='100%')
    grid.add(bar, grid_bottom="60%")
    grid.add(line, grid_top="60%")
    grid.render()

    return grid

