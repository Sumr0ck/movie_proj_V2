from django.urls import path

from . import views

urlpatterns = [
    path('', views.MovieView.as_view(), name='main'),
    path('<slug:slug>/', views.MovieDetailView.as_view(), name='moviesingle'),
    path('review/<int:pk>/', views.AddReview.as_view(), name='add_review'),
]
