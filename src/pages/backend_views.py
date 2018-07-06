from borax.fetch import fetch

from django.db.models import Count
from pyecharts import Line, Pie, Page, Bar
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
        device_data = models.Device.objects.values('device_type').annotate(count=Count('device_type'))
        device_types, counters = fetch(device_data, 'device_type', 'count')
        pie = Pie("設備分類", page_title='設備分類', width='100%')
        pie.add("設備分類", device_types, counters, is_label_show=True)

        #battery_lifes = models.Device.objects.values('name', 'battery_life')
        #names, lifes = fetch(battery_lifes, 'name', 'battery_life')
        #bar = Bar('設備電量', page_title='設備電量', width='100%')
        #bar.add("設備電量", names, lifes)
        
        gap_avg = models.FilmParameter.objects.aggregate(
            avg1=m.Avg('gap1'),
            avg2=m.Avg('gap2'),
            avg3=m.Avg('gap3'),
            avg4=m.Avg('gap4')
        )
        bar = Bar('間距(寬度)', page_title='間距', width='100%')
        for i in range(1, 5):
            bar.add(f"gap{i}", [f"gap{i}"], [gap_avg[f"avg{i}"]])

        page = Page.from_charts(pie, bar)
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
