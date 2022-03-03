from django.urls import path

from . import views

urlpatterns = [
    path('', views.MovieView.as_view(), name='main'),
    path('filter/', views.FilterMoviesView.as_view(), name='filter'),
    path('<slug:slug>/', views.MovieDetailView.as_view(), name='moviesingle'),
    path('review/<int:pk>/', views.AddReview.as_view(), name='add_review'),
    path('actor/<str:slug>/', views.ActorView.as_view(), name='actor_detail'),
]
