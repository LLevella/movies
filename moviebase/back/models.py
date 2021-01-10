from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Actor(models.Model):
    """Актеры и режиссеры"""
    name = models.CharField("Имя", max_length=100)
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="actors/")

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('actor_detail', kwargs={"slug": self.name})

    class Meta:
        verbose_name = "Актеры и режиссеры"
        verbose_name_plural = "Актеры и режиссеры"


class Genre(models.Model):
    """Жанры"""
    name = models.CharField("Имя", max_length=100)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Movie(models.Model):
    """Фильм"""
    title = models.CharField("Название", max_length=100)
    description = models.TextField("Описание")
    poster = models.ImageField("Постер", upload_to="images/")
    year = models.PositiveSmallIntegerField("Дата выхода", default=2021)
    country = models.CharField("Страна", max_length=30)
    directors = models.ManyToManyField(Actor, verbose_name="режиссер", related_name="film_director")
    actors = models.ManyToManyField(Actor, verbose_name="актеры", related_name="film_actor")
    genres = models.ManyToManyField(Genre, verbose_name="жанры")
    film = models.FileField("Просмотр", upload_to="files/")
    url = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField("Черновик", default=False)
    
    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse("movie_detail", kwargs={"slug": self.url})
    
    # def get_player_url(self):
    #     return reverse('player', kwargs={"slug": self.url})


    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"

class MoviePlayer(models.Model):
    """Плеер фильма"""
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, verbose_name="Фильм", on_delete=models.CASCADE)
    pointer = models.IntegerField("Секунд", default=0)
    
    class Meta:
        unique_together = (('user', 'movie'),)
        verbose_name = "Прогресс просмотра фильма"
        verbose_name_plural = "Прогрессы просмотров фильмов"