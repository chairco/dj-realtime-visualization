# films/factories.py
from films.models import Film, FilmGap, FilmLen, FilmSeq

from factory.fuzzy import FuzzyChoice, FuzzyInteger

from factory.django import DjangoModelFactory


class FilmFactory(DjangoModelFactory):

    class Meta:
        model = Film


class FilmGapFactory(DjangoModelFactory):

    class Meta:
        model = FilmGap


class FilmLenFactory(DjangoModelFactory):

    class Meta:
        model = FilmLen


class FilmSeqFactory(DjangoModelFactory):

    class Meta:
        model = FilmSeq


