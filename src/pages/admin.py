#films/admin.py
from django.contrib import admin

from pages.models import Device, FilmParameter, Blog

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


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'content',
        'post_time', 'read_count'
    ]