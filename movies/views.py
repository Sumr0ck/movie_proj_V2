from django.shortcuts import render
from django.views.generic import ListView, DetailView, View

from .models import Movie

# Create your views here.
class MovieView(ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    # template_name = 'movies/movie_list.html'

class MovieDetailView(DetailView):
    """Полное описание фильма"""
    model = Movie
    slug_field = 'url'
    template_name = 'movies/moviesingle.html'
