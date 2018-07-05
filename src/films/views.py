# films/views.py
from django.shortcuts import render
from django.utils.safestring import mark_safe

import json


def index(request):
    return render(request, 'films/index.html', {})


def asyncroom(request, room_name):
    return render(request, 'films/async_room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })


def syncroom(request, room_name):
    return render(request, 'films/sync_room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })