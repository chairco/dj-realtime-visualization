# films/api_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from films.serializers import FilmSerializer, FilmSerializerGap
from films.models import Message, Film, FilmGap


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
        create film record
        :param format: Format of the film record to return to
        :param requests: request object for creating film
        :return: Returns a film record
        """
        serializer = FilmSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_message, status=status.HTTP_400_BAD_REQUEST)


class FilmGapView(APIView):
    """
    a class based view for creating and fetching gap records
    """
    def get(self, format=None):
        """
        """
        films_gap = FilmGap.objects.all()
        serializer = FilmSerializerGap(films_gap, many=True)
        return Response(serializer.data)

    def post(self, request):
        pass


class FilmLenView(APIView):
    """
    a class based view for creating and fetching gap records
    """
    def get(self, format=None):
        """
        """
        films_len = FilmLen.objects.all()
        serializer = FilmSerializerGap(films_len, many=True)
        return Response(serializer.data)

    def post(self, request):
        pass
