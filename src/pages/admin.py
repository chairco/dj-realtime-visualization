#films/admin.py
from django.contrib import admin

from pages.models import Blog

from import_export.admin import ImportExportMixin, ExportActionModelAdmin, ImportExportModelAdmin
from import_export import resources, widgets, fields


class BlogResource(resources.ModelResource):

    class Meta:
        model = Blog
        fields = ('title', 'content')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'content',
        'post_time', 'read_count'
    ]