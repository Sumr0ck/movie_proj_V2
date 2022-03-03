from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View

from .models import Movie, Reviews, Category
from .forms import ReviewForm

# Create your views here.
class MovieView(ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    # extra_context = {'categories': Category.objects.all()}
    # template_name = 'movies/movie_list.html'


class MovieDetailView(DetailView):
    """Полное описание фильма"""
    model = Movie
    slug_field = 'url'
    # extra_context = {'categories': Category.objects.all()}
    template_name = 'movies/moviesingle.html'


class AddReview(View):
    """Отзывы"""
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())
