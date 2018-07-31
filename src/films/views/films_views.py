# films/films_views.py
from borax.fetch import fetch

from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.db.models import Count
from django.core.serializers.json import DjangoJSONEncoder

from django_echarts.views.backend import EChartsBackendView

from pyecharts import Line, Pie, Page, Bar, Boxplot

from films.models import FilmGap, FilmLen, FilmType, Film
from pages.models import FilmParameter

import json


class FilmGapView(EChartsBackendView):
    echarts_instance_name = 'page'
    template_name = 'films/films_gap.html'

    def get_echarts_instance(self, *args, **kwargs):
        decimal_places = 3
        film_datas = FilmGap.objects.all()
        ids = fetch(film_datas.values("id"), "id")

        # boxplot
        boxplot = Boxplot('間距', page_title='(盒鬚圖)', width='100%')        
        x_axis = ['gap0', 'gap1', 'gap2', 'gap3', 'gap4', 'gap5']
        y_axis = [
            list(filter(lambda x:x>1, fetch(film_datas.values(f"gap{i}"), f"gap{i}"))) 
            for i in range(1, 5)
        ]
        _yaxis = boxplot.prepare_data(y_axis)  # JSON serializable
        boxplot.add(
            "Film gaps",
            x_axis, 
            _yaxis,
        )

        attr = ids
        bar_mix = Bar("Gap長度", page_title='(長條圖)', width='100%')
    
        for i in range(1, 5):
            bar_data = fetch(film_datas.values(f"gap{i}"), f"gap{i}")
            bar_mix.add(
                f"gap{i}",
                attr,
                list(map(lambda x:round(x, decimal_places), bar_data)),
                is_stack=True,
                is_datazoom_show=True
            )

        page = Page.from_charts(boxplot, bar_mix)
        return page
