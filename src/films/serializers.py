from rest_framework import serializers

from films.models import Film, FilmGap


class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = (
            'filmid', 'pic', 'pic_url', 'content_type',
            'rs232_time', 'create_time'
        )

    def create(self, validated_data):
        return Film.objects.create(**validated_data)


class FilmSerializerGap(serializers.ModelSerializer):
    film = FilmSerializer(many=False)

    class Meta:
        model = FilmGap
        fields = (
            'gap0', 'gap1', 'gap2', 
            'gap3', 'gap4', 'gap5',
            'film'
        )

    def create(self, validated_data):
        film_datas = validated_data.pop('film')
        filmgap = FilmGap.objects.create(**validated_data)
        for film_data in film_datas:
            Film.objects.create(**validated_data)
        return filmgap

    def update(self, instance, validated_data):
        pass


