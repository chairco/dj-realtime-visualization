# films/tests.py
from django.urls import include, path, reverse

from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase


class FilmTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('films/', include('films.urls')),
    ]

    def test_films_lists(self):
        """
        Ensure films page
        """
        url = reverse('films_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_create_films(self):
        pass
