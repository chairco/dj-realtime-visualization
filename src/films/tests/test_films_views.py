# films/tests.py
import json

from django.urls import include, path, reverse
from django.test import TestCase

from films.models import Film, FilmSeq, FilmType

from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase


class FilmTests(APITestCase, URLPatternsTestCase, TestCase):
    urlpatterns = [
        path('films/', include('films.urls')),

    ]
    def create_filmseq(self):
        return FilmSeq.objects.create()

    def create_filmtype(self, content_type='21050N-20-CP'):
        return FilmType.objects.create(content_type=content_type)

    def test_create_seqs(self):
        url = reverse('films_seq_api')
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_create_films(self):
        filmseq = self.create_filmseq()
        content_type = self.create_filmtype()
        url = reverse('films_views_api')
        payload = {
            'pic': 'Image_C0_00000001',
            'pic_url': '',
            'content_type': content_type.id,
            'seq': filmseq.id,
            'cam': 0,
            'rs232_time': '2018-08-23T08:01:00+08:00',
            'len_ret': '0',
            'gap_ret': '0',
            'film_gaps': {'gap0': 1.72, 'gap1': 1.96,'gap2': 1.97,
                          'gap3': 2.12, 'gap4': 2.02, 'gap5': 1.72},
            'film_lens': {'pink': 45.06, 'orange': 44.32, 'yellow': 45.23,
                          'green': 45.12, 'blue': 45.56}
        }
        resp = self.client.post(url, json.dumps(payload), format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Film.objects.count(), 1)
        self.assertEqual(Film.objects.get().pic, 'Image_C0_00000001')

    def test_films_lists(self):
        """
        Ensure films page
        """
        url = reverse('films_views_api')
        resp = self.client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 0)

