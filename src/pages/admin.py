#films/admin.py
from django.contrib import admin

from .models import Device, FilmParameter

from import_export.admin import ImportExportMixin, ExportActionModelAdmin, ImportExportModelAdmin
from import_export import resources, widgets, fields


class FilmParameterResource(resources.ModelResource):

    class Meta:
        model = FilmParameter
        fields = ('gap0', 'gap1')


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = [
        'mac', 'name', 'address', 
        'battery_life'
    ]


@admin.register(FilmParameter)
class FilmParameterAdmin(ImportExportModelAdmin):
    list_display = [
        'gap0', 'gap1', 'gap2', 'gap3', 'gap4', 'gap5',
        'pink', 'orange', 'yellow', 'green', 'blue'
    ]
