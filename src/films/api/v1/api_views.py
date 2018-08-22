# films/api_views.py
from rest_framework import viewsets, status, mixins, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.request import Request

from django.http import QueryDict

from films.serializers import (FilmSerializer, FilmGapSerializer, 
                                FilmLenSerializer, FilmSeqSerializer)
from films.models import Film, FilmGap, FilmLen, FilmSeq

import json


def get_parameter_dic(request, *args, **kwargs):
    """
    Query parameter
    """
    if isinstance(request, Request) == False:
        return {}

    query_params = request.query_params
    
    if isinstance(query_params, QueryDict):
        query_params = query_params.dict()
    
    result_data = request.data
    
    if isinstance(result_data, QueryDict):
        result_data = result_data.dict()

    if query_params != {}:
        return query_params
    else:
        return result_data


class FilmListMixin(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):
    """
    List all code film, or create a new one.
    """
    queryset = Film.objects.all().order_by('-rs232_time')[:100]
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
    queryset = FilmSeq.objects.all().order_by('seqid')[:100]
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
    def get(self, request, format=None):
        """
        Get all the film records
        :param num: record number, default:latest 100
        :param format: Format of the film records to return to
        :return: Return a list of film records
        """
        num = self.request.query_params.get('num', 100)
        films = Film.objects.all().order_by('-rs232_time')[:int(num)]
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


# below is /api/v1

class FilmViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Get all the all film gap records
    :param format: Format of the film records to return to
    :return: Return a list of film gap records
    """
    queryset = Film.objects.all()
    serializer_class = FilmSerializer


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