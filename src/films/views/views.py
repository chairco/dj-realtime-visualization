# films/views.py
from django.shortcuts import render
from django.utils.safestring import mark_safe

from films.models import Message

import json


def index(request):
    return render(request, 'films/index.html', {})


def asyncroom(request, room_name):
    chat_messages = Message.objects.filter(group_name=f"chats_{room_name}").order_by("created")[:100]
    return render(request, 'films/async_room.html', {
        'chat_messages': chat_messages,
        'room_name_json': mark_safe(json.dumps(room_name))
    })


def syncroom(request, room_name):
    chat_messages = Message.objects.filter(group_name=room_name).order_by("created")[:100]
    return render(request, 'films/sync_room.html', {
        'chat_messages': chat_messages,
        'room_name_json': mark_safe(json.dumps(room_name))
    })


def dashboard(request, room_name):
    chat_messages = Message.objects.filter(group_name=room_name).order_by("created")[:100]
    return render(request, 'films/dashboard.html', {
        'chat_messages': chat_messages,
        'room_name_json': mark_safe(json.dumps(room_name))
    })


