#-*- coding: utf-8 -*-
import datetime
import itertools
import pytz

from borax.fetch import fetch
from pyecharts import Bar, Line, Grid, Scatter, EffectScatter

from films.models import FilmGap, Film
from films.factory import ChartFactory

from django.db.models import Count, Q

from collections import OrderedDict


FACTORYDASH = ChartFactory()


def gen_dates(start, end):
    while start < end:
        start += datetime.timedelta(minutes=1)
        yield start.strftime('%Y-%m-%d %H:%M')


def filmdata_all(hours):
    #latest_film = Film.objects.order_by('-rs232_time')[0]
    #latest_film = latest_film.rs232_time
    #last_time = latest_film - datetime.timedelta(hours=hours) #latest 1h
    
    latest_film = datetime.datetime.now()
    last_time = latest_film - datetime.timedelta(hours=hours) #latest 1h

    film_datas = Film.objects.filter(rs232_time__gte=last_time)

    # UTC to +8, using pytz or timedelta
    #tzutc_8 = datetime.timezone(datetime.timedelta(hours=8))
    tzutc_8 = pytz.timezone('Asia/Taipei')
    
    # count the yield of mins
    grouped = itertools.groupby(film_datas, lambda f: f.rs232_time.astimezone(tzutc_8).strftime("%Y-%m-%d %H:%M"))
    data_records = {day: len(list(g)) for day, g in grouped}
    # get all time interval 
    data_gaps = {d: 0 for d in gen_dates(last_time.astimezone(tzutc_8), latest_film.astimezone(tzutc_8))}
    # combine missing time
    data_all = {**data_gaps, **data_records}
    return data_all


@FACTORYDASH.collect('dash')
def create_dash(hours):
    """
    create bar+line to show yield rate in the time interval
    """
    data_all = filmdata_all(hours=hours)
    # sort data by key
    data_filter = OrderedDict(sorted(data_all.items(), key=lambda t: t[0]))

    attr = list(data_filter.keys())
    cam0 = list(data_filter.values())
    
    bar = Bar("產能柱狀圖", height=720)
    bar.add("cam0", attr, cam0, 
        is_stack=True, 
        is_datazoom_show=True, 
        datazoom_xaxis_index=[0, 1],
    )

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


@FACTORYDASH.collect('dash_yield')
def create_dash_yield(hours):
    """
    create bar+line to show yield rate in the time interval
    """

    data_all = filmdata_all(hours=hours)
    # sort data by key
    data_filter = OrderedDict(sorted(data_all.items(), key=lambda t: t[0]))

    attr = list(data_filter.keys())
    cam0 = list(data_filter.values())
    
    bar = Bar("產能柱狀圖", height=720)
    bar.add(
        "cam0", attr, cam0, 
        is_stack=True, 
    )
    
    line = Line("產能折線圖", title_top="50%")
    line.add(
        "cam0", attr, cam0,
        mark_point=["max", "min"],
        mark_line=["average"],
    )
    
    grid = Grid(width='100%')
    grid.add(bar, grid_bottom="60%")
    grid.add(line, grid_top="60%")
    grid.render()

    return grid


@FACTORYDASH.collect('dash_scatter')
def create_dash_scatter(hours):
    data_all = filmdata_all(hours=hours)
    # sort data by key
    data_filter = OrderedDict(sorted(data_all.items(), key=lambda t: t[1]))
    
    groups = itertools.groupby(data_filter.values())
    groups_dict = {k: len(list(v)) for k, v in groups}

    v1 = list(groups_dict.keys())
    v2 = list(groups_dict.values())
    
    scatter = Scatter(width=1200)
    scatter.add(
        "稼動s", 
        v1, v2,
        is_visualmap=True,
        visual_dimension=1,
        visual_orient="horizontal",
        visual_type="size",
        visual_range=[0, 14],
        visual_text_color="#000",
        legend_pos="70%"
    )
    
    order_group_dict = OrderedDict(sorted(groups_dict.items(), key=lambda t: t[0]))
    
    target = max(order_group_dict.keys())
    vv1 = [target]
    vv2 = [order_group_dict.get(target)]

    es = EffectScatter()
    es.add(
        "稼動es",
        vv1,
        vv2,
        effect_scale=6,
        legend_pos="20%",
    )
    
    grid = Grid(width='100%')
    grid.add(scatter, grid_left="60%")
    grid.add(es, grid_right="60%")
    grid.render()

    return grid

