# films/tests/test_films_models.py
from django.test import TestCase
from films.models import Film, FilmSeq, FilmType

from datetime import datetime


class FilmsTest(TestCase):

    def create_filmtype(self, content_type='21050N-20-CP'):
        return FilmType.objects.create(content_type=content_type)

    def test_filmtype_creation(self):
        content_type = self.create_filmtype()
        self.assertTrue(isinstance(content_type, FilmType))
        self.assertEqual(content_type.__str__(), content_type.content_type)

    def create_filmseq(self):
        return FilmSeq.objects.create()

    def test_filmseq_creation(self):
        filmseq = self.create_filmseq()
        self.assertTrue(isinstance(filmseq, FilmSeq))
        self.assertEqual(filmseq.__str__(), str(filmseq.id))

    def create_film(self, pic='Image_C0_00000001', pic_url='', 
                    cam=0, rs232_time='2018-08-23T08:01:00+08:00',
                    len_ret='PASS', gap_ret='PASS'):

        filmseq = self.create_filmseq()
        content_type = self.create_filmtype()
        return Film.objects.create(
            pic=pic, pic_url=pic_url, content_type=content_type,
            seq=filmseq, cam=cam, rs232_time=rs232_time, len_ret=len_ret,
            gap_ret=gap_ret
        )

    def test_film_creation(self):
        film = self.create_film()
        self.assertTrue(isinstance(film, Film))
        self.assertEqual(film.__str__(), film.pic)