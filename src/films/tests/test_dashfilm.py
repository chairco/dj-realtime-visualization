# films/tests.py
import pytz
import pytest
import itertools

from datetime import datetime

from django.test import TestCase
from django.utils import timezone

from films.models import Film
from films.load_dashdata import filmsgroupy


pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class FilmDashTest(TestCase):
    pytestmark = pytest.mark.django_db

    def setUp(self):
        super(FilmDashTest, self).setUp()
        self.tzutc_8 = pytz.timezone('Asia/Taipei')
        self.dt = '2018-09-07 12:38'
        self.films = Film.objects.all()

    def test_filmsgroupy(self):
        """
        test groupy
        """
        latest_film = datetime.strptime(
            '2018-09-07 12:38', '%Y-%m-%d %H:%M').replace(tzinfo=self.tzutc_8)
        last_time = latest_film - timezone.timedelta(hours=1)
        film_datas = Film.objects.filter(
            rs232_time__gte=last_time).order_by('-rs232_time')

        start = last_time.astimezone(self.tzutc_8)
        end = latest_film.astimezone(self.tzutc_8)
        data_all = filmsgroupy(film_datas, start, end)
        self.assertEqual(sum(list(data_all.values())), 0)

    def test_db(self):
        """
        """
        films = Film.objects.all()
        self.assertEqual(len(films), 0)
