# films/api_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser

from rest_framework import mixins
from rest_framework import generics

from films.serializers import FilmSerializer, FilmSerializerGap
from films.models import Message, Film, FilmGap, FilmLen

import json


class FilmList(mixins.ListModelMixin,
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


class FilmView(APIView):
    """
    a class based view for creating and fetching film records
    """
    #parser_classes = (JSONParser,)
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
        create film record
        :param format: Format of the film record to return to
        :param requests: request object for creating film
        :return: Returns a film record
        """
        print(request.data)
        if isinstance(request.data, dict):
            data = request.data
        else:
            data = json.loads(request.data)
        
        serializer = FilmSerializer(data=data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_message, status=status.HTTP_400_BAD_REQUEST)


class FilmGapView(APIView):
    """
    a class based view for creating and fetching gap records
    """
    def get(self, format=None):
        """
        Get all the filmgap records
        :param format: Format of the filmgap records to return to
        :return: Return a list of filmgap records
        """
        films_gap = FilmGap.objects.all()
        serializer = FilmSerializerGap(films_gap, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        create filmgap record
        :param format: Format of the filmgap record to return to
        :param requests: request object for creating filmgap
        :return: Returns a filmgap record
        """
        serializer = FilmSerializerGap(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_message, status=status.HTTP_400_BAD_REQUEST)


class FilmLenView(APIView):
    """
    a class based view for creating and fetching gap records
    """
    def get(self, format=None):
        """
        Get all the filmlen records
        :param format: Format of the filmlen records to return to
        :return: Return a list of filmlen records
        """
        films_len = FilmLen.objects.all()
        serializer = FilmSerializerGap(films_len, many=True)
        return Response(serializer.data)


