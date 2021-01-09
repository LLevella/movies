from django.db import models
from movies.models import Movie

# Create your models here.

class MoviePlayer(Movie):
    """Плеер фильма"""
    pointer = models.SmallIntegerField("Указатель на смещение", default=0)
