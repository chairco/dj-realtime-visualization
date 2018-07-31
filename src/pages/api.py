# pages/api.py
from rest_framework import viewsets, serializers, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import Http404

from pages.models import FilmParameter
from pages.serializers import FilmGapSerializer


from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


@csrf_exempt
def film_list(request):
    if request.method == 'GET':
        filmparameters = FilmParameter.objects.all()
        serializer = FilmGapSerializer(filmparameters, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = FilmGapSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class FilmList(APIView):
    """
    """
    def get(self, request, format=None):
        filmparameters = FilmParameter.objects.all()
        serializer = FilmGapSerializer(filmparameters, many=True)
        return Response(serializer.data)

    def post(self, requests, format=None):
        serializer = FilmGapSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


class FilmDetail(APIView):
    """
    """
    def get_object(self, pk):
        pass

    def get(self, requests, pk, format=None):
        pass

    def put(self, requests, pk, format=None):
        pass

    def delete(self, requests, pk, format=None):
        pass 