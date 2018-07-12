#pages/models
from django.db import models
from django.utils import timezone

from django_echarts.datasets.managers import AxisValuesQuerySet


class Device(models.Model):
    mac = models.CharField(max_length=50, unique=True, verbose_name="MAC Address", )
    name = models.CharField(max_length=50, default='-', verbose_name="設備名稱")
    device_type = models.CharField(max_length=50, verbose_name="設備類型")
    latitude = models.FloatField(null=True, blank=True, verbose_name="經度")
    longitude = models.FloatField(null=True, blank=True, verbose_name="緯度")
    address = models.CharField(max_length=50, null=True, blank=True, verbose_name="Install Address")
    battery_life = models.IntegerField(verbose_name='電量(%)', default=100)
    online = models.NullBooleanField(default=None, verbose_name="線上狀態")
    parent_gateway_mac = models.CharField(max_length=50, blank=True, null=True)
    parent_rtu_mac = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.mac


class DataRecord(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    record_time = models.DateTimeField(default=timezone.now)
    val1 = models.IntegerField()
    val2 = models.IntegerField()

    def __str__(self):
        return 'Data Record {0}'.format(self.device.mac)


class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    author = models.CharField(max_length=50)
    post_time = models.DateTimeField(default=timezone.now)
    read_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class TemperatureRecord(models.Model):
    high = models.FloatField()
    low = models.FloatField()
    create_time = models.DateTimeField(default=timezone.now)

    objects = models.Manager.from_queryset(AxisValuesQuerySet)()

    def __str__(self):
        return 'Temperature Record'


class FilmParameter(models.Model):
    gap0 = models.FloatField(null=True, blank=True, verbose_name="左邊|粉色")
    gap1 = models.FloatField(null=True, blank=True, verbose_name="粉色|橘色")
    gap2 = models.FloatField(null=True, blank=True, verbose_name="橘色|黃色")
    gap3 = models.FloatField(null=True, blank=True, verbose_name="黃色|綠色")
    gap4 = models.FloatField(null=True, blank=True, verbose_name="綠色|藍色")
    gap5 = models.FloatField(null=True, blank=True, verbose_name="藍色|右邊")
    
    pink = models.FloatField(null=True, blank=True, verbose_name="粉色")
    orange = models.FloatField(null=True, blank=True, verbose_name="橘色")
    yellow = models.FloatField(null=True, blank=True, verbose_name="黃色")
    green = models.FloatField(null=True, blank=True, verbose_name="綠色")
    blue = models.FloatField(null=True, blank=True, verbose_name="藍色")
    
    create_time = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return "Film Parameter"

