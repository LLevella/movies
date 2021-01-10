from rest_framework import serializers

from .models import Movie, Genre, Actor, MoviePlayer


class ActorListSerializer(serializers.ModelSerializer):
    """Вывод списка актеров и режиссеров"""
    class Meta:
      model = Actor
      fields = ("id", "name", "image")


class ActorDetailSerializer(serializers.ModelSerializer):
    """Вывод полного описани актера или режиссера"""
    class Meta:
      model = Actor
      fields = "__all__"

class GenresDetailSerializer(serializers.ModelSerializer):
    """Вывод жанров"""
    class Meta:
      model = Genre
      fields = "__all__"

class GenresSerializer(serializers.ModelSerializer):
    """Вывод жанров"""
    class Meta:
      model = Genre
      fields = ("id", "name")

class MovieListSerializer(serializers.ModelSerializer):
    """Список фильмов"""
    class Meta:
      model = Movie
      fields = ("id", "title","poster")

class MovieDetailSerializer(serializers.ModelSerializer):
    """Полный фильм"""
    directors = ActorListSerializer(read_only=True, many=True)
    actors = ActorListSerializer(read_only=True, many=True)
    genres = GenresSerializer(read_only=True, many=True)

    class Meta:
      model = Movie
      exclude = ("draft",)


class MoviePlayerSerializer(serializers.ModelSerializer):
  """Время просмотра фильма"""
  class Meta:
    model = MoviePlayer
    fields = "__all__"
  
  def create(self, validated_data):
    player = MoviePlayer.objects.update_or_create(
        user=validated_data.get('user', None),
        movie=validated_data.get('movie', None),
        defaults={'pointer': validated_data.get("pointer")}
    )
    print(player)
    return player

  def partial_update(self, validated_data):
    player = MoviePlayer.objects.partial_update(
        id=validated_data.get('id', None),
        defaults={'pointer': validated_data.get("pointer")}
    )
    print(player)
    return player