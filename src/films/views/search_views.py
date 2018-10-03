from films.models import Film
from django.shortcuts import render
from films.filters import FilmFilter

from django_filters.views import FilterView


def search(request):
    film_list = Film.objects.all()
    film_filter = FilmFilter(request.GET, queryset=film_list)
    return render(request, 'films/search.html', {'filter': film_filter})


class FilmSearch(FilterView):
    filterset_class = FilmFilter
    template_name = 'films/search.html'
    paginate_by = 10