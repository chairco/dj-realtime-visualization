from borax.fetch import fetch

from django.db.models import Count
from pyecharts import Line, Pie, Page, Bar, Boxplot
from django_echarts.datasets.charts import NamedCharts
from django_echarts.views.backend import EChartsBackendView
from django.db import models as m

from . import models

from .demo_data import FACTORY


class BackendEChartsTemplate(EChartsBackendView):
    template_name = 'pages/backend_charts.html'

    def get_echarts_instance(self, *args, **kwargs):
        name = self.request.GET.get('name', 'bar')
        return FACTORY.create(name)

    def get_template_names(self):
        if self.request.GET.get('name') == 'word_cloud':
            return ['pages/word_cloud.html']
        else:
            return super().get_template_names()


class TemperatureEChartsView(EChartsBackendView):
    echarts_instance_name = 'line'
    template_name = 'pages/temperature_charts.html'

    def get_echarts_instance(self, **kwargs):
        t_data = models.TemperatureRecord.objects.all().order_by('create_time').values_list('high', 'create_time')
        hs, ds = zip(*t_data)
        line = Line('High Temperature')
        line.add('High', ds, hs)
        return line


class PageDemoView(EChartsBackendView):
    echarts_instance_name = 'page'
    template_name = 'pages/page_demo.html'

    def get_echarts_instance(self, *args, **kwargs):
        decimal_places = 3
        # Boxplot
        boxplot = Boxplot('間距', page_title='(盒鬚圖)', width='100%')        
        x_axis = ['gap1', 'gap2', 'gap3', 'gap4']
        film_datas = models.FilmParameter.objects.all()
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
        
        # Bar mix
        bar = Bar('間距', page_title='(長條圖)', width='100%')
        gap_avg = models.FilmParameter.objects.aggregate(
            avg1=m.Avg('gap1'),
            avg2=m.Avg('gap2'),
            avg3=m.Avg('gap3'),
            avg4=m.Avg('gap4')
        )
        for i in range(1, 5):
            bar_avg_data = [gap_avg[f"avg{i}"]]
            bar.add(f"gap{i}", [f"gap"], list(map(lambda x:round(x, decimal_places), bar_avg_data)))

        # Line mix
        line = Line('間距', page_title='(折線圖)' ,width='100%')
        ids = fetch(film_datas.values("id"), "id")
        for i in range(1, 5):
            line_data = fetch(film_datas.values(f"gap{i}"), f"gap{i}")
            line.add(
                f"gap{i}",
                ids, 
                list(map(lambda x:round(x, decimal_places), line_data)), 
                mark_point=["max", "min"], mark_line=["average"],
                is_datazoom_show=True
            )

        # Bar mix
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


        colors = ["pink", "orange", "yellow", "green", "blue"]
        
        # Bar mix
        bar_film = Bar('色條', page_title='(長條圖)', width='100%')
        gap_avg = models.FilmParameter.objects.aggregate(
            pink=m.Avg('pink'),
            orange=m.Avg('orange'),
            yellow=m.Avg('yellow'),
            green=m.Avg('green'),
            blue=m.Avg('blue'),
        )
        for color in colors:
            bar_film_avg_data = [gap_avg[f"{color}"]]
            bar_film.add(f"{color}", [f"{color}"], list(map(lambda x:round(x, decimal_places), bar_film_avg_data)))
  
        # Bar mix
        attr = ids
        bar_len = Bar("色條長度", page_title='(長條圖)', width='100%')
        for color in colors:
            bar_len.add(
                f"{color}",
                attr,
                fetch(film_datas.values(f"{color}"), f"{color}"),
                is_stack=True,
                is_datazoom_show=True
            )
        page = Page.from_charts(boxplot, bar, line, bar_mix, bar_len, bar_film)
        return page


class NamedChartsView(EChartsBackendView):
    echarts_instance_name = 'charts'
    template_name = 'pages/kmultiple_charts.html'

    def get_echarts_instance(self, *args, **kwargs):
        device_data = models.Device.objects.values('device_type').annotate(count=Count('device_type'))
        device_types, counters = fetch(device_data, 'device_type', 'count')
        pie = Pie("設備分類", page_title='設備分類', width='100%')
        pie.add("設備分類", device_types, counters, is_label_show=True)

        battery_lifes = models.Device.objects.values('name', 'battery_life')
        names, lifes = fetch(battery_lifes, 'name', 'battery_life')
        bar = Bar('設備電量', page_title='設備電量', width='100%')
        bar.add("設備電量", names, lifes)
        charts = NamedCharts().add_chart(pie, name='pie').add_chart(bar, name='bar')
        return charts
