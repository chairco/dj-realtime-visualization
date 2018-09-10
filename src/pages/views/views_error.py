# pages/views_error.py
from django.shortcuts import render


def http403(request):
    return render(request, '403.html')