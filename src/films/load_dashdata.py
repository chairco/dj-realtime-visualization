#-*- coding: utf-8 -*-
import datetime
import itertools
import pytz

from borax.fetch import fetch
from pyecharts import Bar, Pie, Line, Grid, Style

from films.models import FilmGap, Film
from films.factory import ChartFactory

from django.db.models import Count, Q

from collections import OrderedDict


FACTORYDASH = ChartFactory()


def gen_dates(start, end):
    while start < end:
        start += datetime.timedelta(minutes=1)
        yield start.strftime('%Y-%m-%d %H:%M')


@FACTORYDASH.collect('dash')
def create_dash(hours):
    """
    create bar+line to show yield rate in the time interval
    """
    latest_film = Film.objects.order_by('-rs232_time')[0]
    last_time = latest_film.rs232_time - datetime.timedelta(hours=hours) #latest 24h
    film_datas = Film.objects.filter(rs232_time__gte=last_time)

    # UTC to +8, using pytz or timedelta
    #tzutc_8 = datetime.timezone(datetime.timedelta(hours=8))
    tzutc_8 = pytz.timezone('Asia/Taipei')
    
    # count the yield of mins
    grouped = itertools.groupby(film_datas, lambda f: f.rs232_time.astimezone(tzutc_8).strftime("%Y-%m-%d %H:%M"))
    data_records = {day: len(list(g)) for day, g in grouped}
    # get all time interval 
    data_gaps = {d: 0 for d in gen_dates(last_time.astimezone(tzutc_8), latest_film.rs232_time.astimezone(tzutc_8))}
    # combine missing time
    data_all = {**data_gaps, **data_records}
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