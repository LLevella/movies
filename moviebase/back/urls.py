from django.urls import path

from . import views

urlpatterns = [
    path("detail/", views.MovieDetailView.as_view()),
    # path("player/<int:movie_id>/<int:user_id>", views.MoviePlayerView.as_view()),
    path("player/", views.MoviePlayerView.as_view()),
    path("", views.MovieListView.as_view()),
]
