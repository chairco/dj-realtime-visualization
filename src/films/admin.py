# films/admin.py
from django.contrib import admin

from .models import Message, Film, FilmGap, FilmLen, FilmWidth, FilmType, FilmSeq

# Register your models here.

class FilmGapInline(admin.TabularInline):
    model = FilmGap
    extra = 1


class FilmLenInline(admin.TabularInline):
    model = FilmLen
    extra = 1


class FilmWidthInline(admin.TabularInline):
    model = FilmWidth
    extra = 1


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [
            'user', 'group_name',
            'message', 'created'
        ]


@admin.register(FilmType)
class FilmTypeAdmin(admin.ModelAdmin):
    list_display = ['content_type']


@admin.register(FilmSeq)
class FilmSeqAdmin(admin.ModelAdmin):
    list_display = ['seqid', 'create_time']
    list_display_links = None


@admin.register(FilmGap)
class FilmGapAdmin(admin.ModelAdmin):
    list_display = [
        'film', 'gap0', 'gap1', 'gap2',
        'gap3', 'gap4', 'gap5'
    ]
    list_display_links = None


@admin.register(FilmLen)
class FilmLenAdmin(admin.ModelAdmin):
    list_display = [
        'film', 'pink', 'orange', 'yellow',
        'green', 'blue'
    ]
    list_display_links = None


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = [
        'filmid', 'pic', #'pic_url',
        'content_type', 'seq', 'cam',
        'rs232_time', 'create_time',
    ]
    inlines = (
        FilmGapInline, 
        FilmLenInline, 
        FilmWidthInline, 
    )

