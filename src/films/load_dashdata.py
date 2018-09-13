#-*- coding: utf-8 -*-
import datetime
import itertools
import pytz

from borax.fetch import fetch
from pyecharts import Bar, Line, Grid, Scatter, EffectScatter

from films.models import FilmGap, Film
from films.factory import ChartFactory

from django.db.models import Count, Q
from django.utils import timezone

from collections import OrderedDict


FACTORYDASH = ChartFactory()


def gen_dates(start, end):
    while start < end:
        start += datetime.timedelta(minutes=1)
        yield start.strftime('%Y-%m-%d %H:%M')


def filmsgroupy(film_datas, start, end):
    """
    """
    # UTC to +8, using pytz or timedelta
    tzutc_8 = pytz.timezone('Asia/Taipei')

    # group by mins, data should be order by rs232 time
    grouped = itertools.groupby(film_datas, lambda f: f.rs232_time.astimezone(
        tzutc_8).strftime("%Y-%m-%d %H:%M"))
    data_records = {day: len(list(g)) for day, g in grouped}
    # get all time interval
    data_gaps = {d: 0 for d in gen_dates(start, end)}
    data_all = {**data_gaps, **data_records}
    return data_all


def filmdata_gap(start, end, cam=None):
    """
    film gap
    """
    # UTC to +8, using pytz or timedelta
    tzutc_8 = pytz.timezone('Asia/Taipei')

    start = datetime.datetime.strptime(
        start, '%Y-%m-%d %H:%M').astimezone(tzutc_8)
    end = datetime.datetime.strptime(
        end, '%Y-%m-%d %H:%M').astimezone(tzutc_8)
    if not cam:
        film_datas = Film.objects.filter(Q(rs232_time__gte=start), Q(
            rs232_time__lte=end)).order_by('-rs232_time')
    else:
        film_datas = Film.objects.filter(Q(rs232_time__gte=start), Q(
            rs232_time__lte=end), Q(cam=cam)).order_by('-rs232_time')
    data_all = filmsgroupy(film_datas, start, end)
    return data_all


def filmdata_all(hours, cam=None):
    """
    film data
    """
    # UTC to +8, using pytz or timedelta
    tzutc_8 = pytz.timezone('Asia/Taipei')
    # find data by time
    latest_film = timezone.now()
    last_time = latest_film - timezone.timedelta(hours=hours)  # latest 1h
    if not cam:
        film_datas = Film.objects.filter(Q(
            rs232_time__gte=last_time)).order_by('-rs232_time')
    else:
        film_datas = Film.objects.filter(Q(
            rs232_time__gte=last_time), Q(cam=cam)).order_by('-rs232_time')
    start = last_time.astimezone(tzutc_8)
    end = latest_film.astimezone(tzutc_8)
    data_all = filmsgroupy(film_datas, start, end)
    return data_all


@FACTORYDASH.collect('dash')
def create_dash(**kwargs):
    """
    create bar+line to show yield rate in the time interval
    """
    start = kwargs.get('start')
    end = kwargs.get('end')
    hours = kwargs.get('hours')
    
    if start and end:
        #data_all = filmdata_gap(start=start, end=end)
        data_cam0 = filmdata_gap(start=start, end=end, cam=0)
        data_cam1 = filmdata_gap(start=start, end=end, cam=1)
    elif start or end:
        #data_all = {}
        data_cam0 = {}
        data_cam1 = {}
    else:
        #data_all = filmdata_all(hours=hours)
        data_cam0 = filmdata_all(hours=hours, cam=0)
        data_cam1 = filmdata_all(hours=hours, cam=1)
    
    # sort data by key
    #data_filter = OrderedDict(sorted(data_all.items(), key=lambda t: t[0]))
    data_filter_cam0 = OrderedDict(sorted(data_cam0.items(), key=lambda t: t[0]))
    data_filter_cam1 = OrderedDict(sorted(data_cam1.items(), key=lambda t: t[0]))

    attr_cam0 = list(data_filter_cam0.keys())
    cam0 = list(data_filter_cam0.values())

    attr_cam1 = list(data_filter_cam1.keys())
    cam1 = list(data_filter_cam1.values())


    bar = Bar("產能柱狀圖", height=720)
    bar.add("cam0", attr_cam0, cam0,
            is_stack=True,
            is_datazoom_show=True,
            datazoom_xaxis_index=[0, 1],
            )
    bar.add("cam1", attr_cam1, cam1,
        is_stack=True,
        is_datazoom_show=True,
        datazoom_xaxis_index=[0, 1],
        )

    line = Line("產能折線圖", title_top="50%")
    line.add(
        "cam0", attr_cam0, cam0,
        mark_point=["max", "min"],
        mark_line=["average"],
        legend_top="50%",
        is_datazoom_show=True,
    )
    line.add(
        "cam0", attr_cam1, cam1,
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
    data_cam0 = filmdata_all(hours=hours, cam=0)
    data_cam1 = filmdata_all(hours=hours, cam=1)

    # sort data by key
    data_filter_cam0 = OrderedDict(sorted(data_cam0.items(), key=lambda t: t[0]))
    data_filter_cam1 = OrderedDict(sorted(data_cam0.items(), key=lambda t: t[0]))

    attr_cam0 = list(data_filter_cam0.keys())
    cam0 = list(data_filter_cam0.values())

    attr_cam1 = list(data_filter_cam1.keys())
    cam1 = list(data_filter_cam1.values())

    bar = Bar("產能柱狀圖", height=720)
    bar.add(
        "cam0", attr_cam0, cam0,
        is_stack=True,
    )
    bar.add(
        "cam1", attr_cam0, cam1,
        is_stack=True,
    )

    line = Line("產能折線圖", title_top="50%")
    line.add(
        "cam0", attr_cam0, cam0,
        mark_point=["max", "min"],
        mark_line=["average"],
    )
    line.add(
        "cam1", attr_cam1, cam1,
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

    order_group_dict = OrderedDict(
        sorted(groups_dict.items(), key=lambda t: t[0]))
    #import operator
    #target = max(a.items(), key=operator.itemgetter(1))[0]
    target = max(order_group_dict, key=order_group_dict.get)
    vv1 = [target]
    vv2 = [order_group_dict.get(target)]

    es = EffectScatter()
    es.add(
        "稼動es",
        vv1,
        vv2,
        effect_scale=5,
        symbol="diamond",
    )

    other_vv1 = list(order_group_dict.keys())
    other_vv1.remove(target)
    other_vv2 = list(order_group_dict.values())
    other_vv2.remove(order_group_dict.get(target))

    es.add(
        "其他稼動es",
        other_vv1,
        other_vv2,
        symbol_size=1,
        effect_scale=2.5,
        effect_period=1,
        symbol="pin",
        legend_pos="20%",
    )

    grid = Grid(width='100%')
    grid.add(scatter, grid_left="60%")
    grid.add(es, grid_right="60%")
    grid.render()

    return grid
