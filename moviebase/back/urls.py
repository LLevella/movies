from django.urls import path

from . import views

urlpatterns = [
    path("detail/<int:movie_id>/", views.MovieDetailView.as_view()),
    path("player/<int:user_id>/<int:movie_id>/",
         views.MoviePlayerView.as_view()),
    path("", views.MovieListView.as_view()),
]
