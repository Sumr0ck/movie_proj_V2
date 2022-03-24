from django.db.models import Q
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import ListView, DetailView, View

from .models import Movie, Category, Actor, Genre, Rating
from .forms import ReviewForm, RatingForm

# Create your views here.
class GenreYear:
    """Жанры и года"""
    def get_genre(self):
        return Genre.objects.all()

    def get_year(self):
        return Movie.objects.filter(draft=False).values('year')


class MovieView(GenreYear, ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False).order_by('id')
    paginate_by = 3
    # extra_context = {'categories': Category.objects.all()}
    # template_name = 'movies/movie_list.html'


class MovieDetailView(GenreYear, DetailView):
    """Полное описание фильма"""
    model = Movie
    slug_field = 'url'
    # extra_context = {'star_form': RatingForm}
    template_name = 'movies/moviesingle.html'

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ip = self.get_client_ip(self.request)
        movie_id = Movie.objects.get(url=self.request.META.get('PATH_INFO').split('/')[-2]).id
        try:
            rating_by_ip = Rating.objects.filter(ip=ip).get(movie_id=movie_id).star_id
        except:
            rating_by_ip = 'Не определенно'
        context['rating_by_ip'] = rating_by_ip
        context['star_form'] = RatingForm()
        context['form'] = ReviewForm()
        return context


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


class ActorView(GenreYear, DetailView):
    """Вывод информации о актере"""
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = 'name'


class FilterMoviesView(GenreYear, ListView):
    """Фильтр фильмов"""
    paginate_by = 2

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist('year')) |
            Q(genres__in=self.request.GET.getlist('genres'))
        ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['year'] = ''.join([f'year={x}&' for x in self.request.GET.getlist('year')])
        context['genres'] = ''.join([f'genres={x}&' for x in self.request.GET.getlist('genres')])
        return context


class AddStarRating(View):
    """Добавление рейтинга к фильму"""

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get('movie')),
                defaults={'star_id': int(request.POST.get('star'))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class Search(GenreYear, ListView):
    """Поиск фильмов"""
    paginate_by = 1

    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get('q').capitalize())

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = f"q={self.request.GET.get('q')}&"
        context['year'] = ''.join([f'year={x}&' for x in self.request.GET.getlist('year')])
        context['genres'] = ''.join([f'genres={x}&' for x in self.request.GET.getlist('genres')])
        return context


class RatingFilterMovies(GenreYear, ListView):
    """Вывод фильмов по рейтингу"""
    paginate_by = 3

    def get_queryset(self):
        return Movie.objects.filter(rating__star__value=self.kwargs.get('pk'))


class CategoryFilter(GenreYear, ListView):
    """Вывод по категориям"""
    paginate_by = 3

    def get_queryset(self):
        return Movie.objects.filter(category__id=self.kwargs.get('pk'))