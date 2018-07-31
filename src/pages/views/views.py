# pages/views.py
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User, Group

from rest_framework import viewsets
from pages.serializers import UserSerializer, GroupSerializer, FilmGapSerializer
from pages.models import FilmParameter


def index(request):
    return render(request, 'index.html', {})


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FilmGapViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows FilmGap to be viewed or edited
    """
    queryset = FilmParameter.objects.all()[:100]
    serializer_class = FilmGapSerializer


