#-*- coding: utf-8 -*-
from borax.fetch import fetch
from pyecharts import Bar, Pie, Line, Grid, Style

from films.models import FilmGap
from films.factory import ChartFactory

from django.db.models import Count, Q


FACTORYGAP = ChartFactory()


@FACTORYGAP.collect('mix')
def create_mix(num):
    pass