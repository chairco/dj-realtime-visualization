#films/filters.py
import django_filters

from films.models import Film


class FilmFilter(django_filters.FilterSet):
    """
    Film filter
    """
    pic = django_filters.CharFilter(
        lookup_expr='icontains'
    )
    
    class Meta:
        model = Film
        fields = ['filmid', 'pic', 'rs232_time',]

    def __init__(self, *args, **kwargs):
        super(FilmFilter, self).__init__(*args, **kwargs)
        # at sturtup user doen't push Submit button, and QueryDict (in data) is empty
        if self.data == {}:
            self.queryset = self.queryset.none()


class FilmApiFilter(django_filters.rest_framework.FilterSet):
    """
    Rest framework filter
    """
    filmid = django_filters.CharFilter(lookup_expr='icontains')
    pic = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Film
        fields = ['filmid', 'pic',]