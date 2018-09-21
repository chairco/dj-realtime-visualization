# films/api_views.py
from rest_framework import viewsets, status, mixins, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.request import Request

from django.http import QueryDict
from django.utils import timezone

from films.serializers import (FilmSerializer, FilmGapSerializer, 
                                FilmLenSerializer, FilmSeqSerializer)
from films.models import Film, FilmGap, FilmLen, FilmSeq

from films.paginations import MyFormatResultsSetPagination

import json
import datetime

# for filter
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework
from rest_framework import filters
from films.filters import FilmApiFilter


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


class FilmSeqList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    """
    class based view(mixins) for creating and fetching film seq
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

class FilmSeqDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    """
    Retrieve, update or delete a film seq instance.
    """
    queryset = FilmSeq.objects.all()
    serializer_class = FilmSeqSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class FilmView(APIView):
    """
    class based view for creating and fetching film records
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


class FilmViewDetail(APIView):
    """
    Retrieve, update or delete a film instance.
    """
    def get_object(self, factory_id):
        try:
            return Film.objects.get(pk=factory_id)
        except Film.DoesNotExist:
            raise Http404

    def get(self, request, factory_id, format=None):
        film = self.get_object(factory_id)
        serializer = FilmSerializer(film)
        return Response(serializer.data)

    def put(self, request, factory_id, format=None):
        film = self.get_object(factory_id)
        serializer = FilmSerializer(film, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, factory_id, format=None):
        film = self.get_object(factory_id)
        film.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DashStatic(APIView):
    """
    A view that returns the count of active users in JSON.
    """
    renderer_classes = (JSONRenderer, )

    def get(self, request, format=None):
        hours = 1
        cam = 2
        # TODO(設定在資料庫)standard yield
        st = 840 * hours * cam
        # now time
        last_time = timezone.now() - timezone.timedelta(hours=hours) #latest 1h
        last_hour_yield = Film.objects.filter(rs232_time__gte=last_time).count()
        last_hour_yield_p = last_hour_yield / st * 100
        downtime = (st - last_hour_yield) * 4 / cam
        content = {
            'last_hour_yield': last_hour_yield,
            'last_hour_yield_p': float('%.2f' %last_hour_yield_p),
            'downtime': float('%.1f' %downtime)
        }
        return Response(content)     


# below is /api/v1

class FilmViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Get all the all film gap records
    :param format: Format of the film records to return to
    :return: Return a list of film gap records
    """
    queryset = Film.objects.all().order_by('-rs232_time')
    serializer_class = FilmSerializer
    pagination_class = MyFormatResultsSetPagination

    #filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter, )
    filter_backends = (rest_framework.DjangoFilterBackend, )
    filter_class = FilmApiFilter
    search_fields = ('filmid', 'pic', 'rs232_time', )
    ordering_fields = ('filmid', 'pic', 'len_ret', 'gap_ret', 'len_ret', )
    ordering = ('-rs232_time', )


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