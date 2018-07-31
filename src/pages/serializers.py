from rest_framework import serializers

from django.contrib.auth.models import User, Group

from pages.models import FilmParameter


class FilmGapSerializer(serializers.Serializer):
    gap0 = serializers.FloatField()
    gap1 = serializers.FloatField()
    gap2 = serializers.FloatField()
    gap3 = serializers.FloatField()
    gap4 = serializers.FloatField()
    gap5 = serializers.FloatField()
    pink = serializers.FloatField()
    orange = serializers.FloatField()
    yellow = serializers.FloatField()
    green = serializers.FloatField()
    blue = serializers.FloatField()

    def create(self, validated_data):
        """
        Create and return a new `FilmParameter` instance, given the validated data.
        """
        return FilmParameter.objects.create(**validated_data)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')