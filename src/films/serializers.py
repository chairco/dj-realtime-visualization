# films/serializers.py
from rest_framework import serializers

from films.models import Film, FilmGap, FilmLen, FilmSeq


class FilmGapSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilmGap
        fields = (
            'gap0', 'gap1', 'gap2', 
            'gap3', 'gap4', 'gap5',
        )


class FilmLenSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilmLen
        fields = (
            'pink', 'orange', 'yellow',
            'green', 'blue',
        )


class FilmSeqSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilmSeq
        fields = ('id', 'seqid',)


class FilmSerializer(serializers.ModelSerializer):
    film_gaps = FilmGapSerializer(many=False)
    film_lens = FilmLenSerializer(many=False)

    class Meta:
        model = Film
        fields = (
            'filmid', 'pic', 'pic_url', 'content_type', 
            'cam', 'seq', 'rs232_time', 'len_ret', 'gap_ret', 
            'film_gaps', 'film_lens'
        )
    
    def create(self, validated_data):
        gap_data = validated_data.pop('film_gaps')
        len_data = validated_data.pop('film_lens')
        film = Film.objects.create(**validated_data)
        FilmGap.objects.create(film=film, **gap_data)
        FilmLen.objects.create(film=film, **len_data)
        return film

    def update(self, instance, validated_data):
        pass

