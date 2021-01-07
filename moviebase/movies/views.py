from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Movie, Actor, Genre

class MoviesView(ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    paginate_by = 1


class MovieDetailView(DetailView):
    """Полное описание фильма"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    slug_field = "url"

class ActorView(DetailView):
    """Вывод информации о актере"""
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = "name"