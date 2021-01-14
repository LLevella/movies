from django.contrib.auth.models import User
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from django.core.cache import cache
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
import json
from .models import Movie, MoviePlayer
from .serializers import MovieListSerializer, MovieDetailSerializer,  MoviePlayerSerializer
import datetime
from .service import (redis_movie_player_db, redis_movies_db, redis_users_db,
                      one_from_many_keys, request_to_obj, quick_check, long_check)


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class MovieListView(APIView):
    """Вывод списка фильмов"""

    def get(self, request):
        movelist = {}
        if 'movielist' in cache:
            movielist = json.loads(cache.get('movielist'))
        else:
            movies = Movie.objects.filter(draft=False)
            if movies.exists():
                serializer = MovieListSerializer(movies, many=True)
                movielist = serializer.data
                cache.set('movielist', json.dumps(
                    movielist), timeout=CACHE_TTL)
            else:
                return Response(movielist, status=status.HTTP_204_NO_CONTENT)
        return Response(movielist, status=status.HTTP_200_OK)


class MovieDetailView(APIView):
    """Вывод фильма"""

    def get(self, request, movie_id):
        movie_data = {}
        movie_key = f'movie:{movie_id}'
        if movie_key in cache:
            movie_data = json.loads(cache.get(movie_key))
        else:
            if Movie.objects.filter(id=movie_id, draft=False).exists():
                movie = Movie.objects.get(
                    id=movie_id, draft=False)
                serializer = MovieDetailSerializer(movie)
                movie_data = serializer.data
                cache.set(movie_key, json.dumps(
                    movie_data), timeout=CACHE_TTL)
            else:
                return Response(movie_data, status=status.HTTP_204_NO_CONTENT)

        if not request.user.is_authenticated:
            # отправим на страницу входа
            movie_data["film"] = f"/auth/token/login"
        return Response(movie_data, status=status.HTTP_200_OK)


class MoviePlayerView(APIView):
    """Добавление времени, обновление, получение времени по фильму и пользователю """
    # в данном случае мы можем коротко запретить доступ не авторизованным
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        mup = request_to_obj(request, ["movie", "user", "pointer"])
        store_dt = datetime.datetime.strftime(
            datetime.datetime.now(datetime.timezone.utc), '%Y-%m-%d %H:%M:%S')

        if not quick_check(redis_users_db, mup["user"]):
            if long_check(User, id=mup["user"]):
                redis_users_db.set(
                    mup["user"], store_dt)
            else:
                return Response(mup, status=status.HTTP_400_BAD_REQUEST)

        if not quick_check(redis_movies_db, mup["movie"]):
            if long_check(Movie, id=mup["movie"]):
                redis_movies_db.set(
                    mup["movie"], store_dt)
            else:
                return Response(mup, status=status.HTTP_400_BAD_REQUEST)

        key_id = one_from_many_keys([mup["movie"], mup["user"]], ":")
        redis_movie_player_db.set(key_id, mup["pointer"])
        return Response(mup, status=status.HTTP_201_CREATED)

    def get(self, request, user_id, movie_id):
        mup = {}
        mup["movie"] = movie_id
        mup["user"] = user_id
        key_id = one_from_many_keys([str(movie_id), str(user_id)], ":")
        pointer = redis_movie_player_db.get(key_id)
        if pointer:
            mup["pointer"] = pointer
        elif MoviePlayer.objects.filter(movie=mup["movie"], user=mup["user"]).exists():
            player = MoviePlayer.objects.get(
                movie=mup["movie"], user=mup["user"])
            serializer = MoviePlayerSerializer(player)
            mup["pointer"] = serializer.data['pointer']
            redis_movie_player_db.set(key_id,  mup["pointer"])
        else:
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        return Response(mup, status=status.HTTP_200_OK)

    def patch(self, request):
        print(request.data)
        mup = request_to_obj(request, ["movie", "user", "pointer"])
        print(mup)
        key_id = one_from_many_keys([str(mup["movie"]), str(mup["user"])], ":")
        old_pointer = redis_movie_player_db.get(key_id)
        # and и or ленивые => если в Redis есть pointer, то в postgre не пойдем
        if old_pointer or MoviePlayer.objects.filter(movie=mup["movie"], user=mup["user"]).exists():
            return Response(mup, status=status.HTTP_200_OK)
        return Response({"errors": "Movies player is not found"}, status=status.HTTP_400_BAD_REQUEST)
