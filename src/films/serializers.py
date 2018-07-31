from rest_framework import serializers

from films.models import Film, FilmGap


class FilmGapSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilmGap
        fields = (
            'gap0', 'gap1', 'gap2', 
            'gap3', 'gap4', 'gap5',
        )


class FilmSerializer(serializers.ModelSerializer):
    film_gaps = FilmGapSerializer(many=False)

    class Meta:
        model = Film
        fields = (
            'filmid', 'pic', 'pic_url',
            'content_type', 'rs232_time', 'film_gaps'
        )
    
    def create(self, validated_data):
        gap_data = validated_data.pop('film_gaps')
        film = Film.objects.create(**validated_data)
        FilmGap.objects.create(film=film, **gap_data)
        return film
    

class FilmSerializerGap(serializers.ModelSerializer):
    film = FilmSerializer(many=False)

    class Meta:
        model = FilmGap
        fields = (
            'gap0', 'gap1', 'gap2', 
            'gap3', 'gap4', 'gap5',
            'film',
        )

    def create(self, validated_data):
        film_datas = validated_data.pop('film')
        filmgap = FilmGap.objects.create(**validated_data)
        for film_data in film_datas:
            Film.objects.create(**validated_data)
        return filmgap

    def update(self, instance, validated_data):
        pass

