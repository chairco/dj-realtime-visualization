# films/api_views.py
from rest_framework import viewsets, status, mixins, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from films.serializers import (FilmSerializer, FilmGapSerializer, 
                                FilmLenSerializer, FilmSeqSerializer)
from films.models import Film, FilmGap, FilmLen, FilmSeq

import json


class FilmListMixin(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                generics.GenericAPIView):
    """
    List all code film, or create a new one.
    """
    queryset = Film.objects.all()
    serializer_class = FilmSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class FilmSeqMixin(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                generics.GenericAPIView):
    """
    a class based view(mixins) for creating and fetching film records
    """
    queryset = FilmSeq.objects.all()
    serializer_class = FilmSeqSerializer

    def get(self, request, *args, **kwargs):
        """
        Get all the film records
        :param format: Format of the film records to return to
        :return: Return a list of film records
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Create film record
        :param format: Format of the film record to return to
        :param requests: request object for creating film
        :return: Returns a film record
        """
        return self.create(request, *args, **kwargs)


class FilmView(APIView):
    """
    a class based view for creating and fetching film records
    """
    def get(self, format=None):
        """
        Get all the film records
        :param format: Format of the film records to return to
        :return: Return a list of film records
        """
        films = Film.objects.all()
        serializer = FilmSerializer(films, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create film record
        :param format: Format of the film record to return to
        :param requests: request object for creating film
        :return: Returns a film record
        """
        if isinstance(request.data, dict):
            data = request.data
        else:
            data = json.loads(request.data)
        
        serializer = FilmSerializer(data=data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_message, status=status.HTTP_400_BAD_REQUEST)


class FilmGapViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Get all the all film gap records
    :param format: Format of the film records to return to
    :return: Return a list of film gap records
    """
    queryset = FilmGap.objects.all()
    serializer_class = FilmGapSerializer


class FilmLenViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Get all the film len records
    :param format: Format of the film len records to return to
    :return: Return a list of film records
    """
    queryset = FilmLen.objects.all()
    serializer_class = FilmLenSerializer