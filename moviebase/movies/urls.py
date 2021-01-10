from django.urls import path
from django.urls import path, include

from . import views


urlpatterns = [
    path("", views.MoviesView.as_view(), name='movies'),
    path("<slug:slug>/", views.MovieDetailView.as_view(), name="movie_detail"),
    path("actor/<str:slug>/", views.ActorView.as_view(), name="actor_detail"),
    path("player/<str:slug>/",  include("video_preview.urls"), name="player"),
]
