# films/admin.py
from django.contrib import admin

from .models import Film, FilmGap, FilmLen, FilmWidth, FilmType, FilmSeq

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


class FilmInline(admin.TabularInline):
    model = Film
    extra = 1


@admin.register(FilmType)
class FilmTypeAdmin(admin.ModelAdmin):
    list_display = ['content_type']
    inlines = (FilmInline,)


@admin.register(FilmSeq)
class FilmSeqAdmin(admin.ModelAdmin):
    list_display = ['seqid']


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = [
        'filmid', 'pic', 'pic_url',
        'content_type', 'rs232_time'
    ]
    inlines = (
        FilmGapInline, 
        FilmLenInline, FilmWidthInline
    )