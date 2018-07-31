# films/serializers.py
from rest_framework import serializers

from films.models import Film, FilmGap, FilmLen


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


class FilmSerializer(serializers.ModelSerializer):
    film_gaps = FilmGapSerializer(many=False)

    class Meta:
        model = Film
        fields = (
            'filmid', 'pic', 'pic_url', 'content_type', 
            'rs232_time', 'len_ret', 'gap_ret', 'film_gaps'
        )
    
    def create(self, validated_data):
        gap_data = validated_data.pop('film_gaps')
        film = Film.objects.create(**validated_data)
        FilmGap.objects.create(film=film, **gap_data)
        return film

    def update(self, instance, validated_data):
        pass

    