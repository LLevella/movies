from .service import redis_movie_player_db, one_from_many_keys, request_to_obj
from .serializers import MovieListSerializer, MovieDetailSerializer,  MoviePlayerSerializer
from .models import Movie, MoviePlayer

import json

from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView

from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

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

    def get(self, request):
        movie_id = request.data.get("movie")
        movie_data = {}
        movie_key = f'movie:{movie_id}'
        if movie_key in cache:
            movie_data = json.loads(cache.get(movie_key))
        else:
            if Movie.objects.filter(id=request.data.get("movie"), draft=False).exists():
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
            obj["film"] = f"/auth/token/login"
        return Response(obj, status=status.HTTP_200_OK)


class MoviePlayerView(APIView):
    """Добавление времени, обновление, получение времени по фильму и пользователю """
    # в данном случае мы можем коротко запретить доступ не авторизованным
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        mup = request_to_obj(request, ["movie", "user", "pointer"])
        key_id = one_from_many_keys([mup["movie"], mup["user"]], ":")
        redis_movie_player_db.set(key_id, mup["pointer"])
        return Response(mup, status=status.HTTP_201_CREATED)

    def get(self, request):
        mup = request_to_obj(request, ["movie", "user"])
        key_id = one_from_many_keys([mup["movie"], mup["user"]], ":")
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
        mup = request_to_obj(request, ["movie", "user", "pointer"])
        key_id = one_from_many_keys([mup["movie"], mup["user"]], ":")
        old_pointer = redis_movie_player_db.get(key_id)
        # and и or ленивые => если в Redis есть pointer, то в postgre не пойдем
        if old_pointer or MoviePlayer.objects.filter(movie=mup["movie"], user=mup["user"]).exists():
            redis_movie_player_db.set(key_id,  mup["pointer"])
            return Response(mup, status=status.HTTP_200_OK)
        return Response({"errors": "Movies player is not found"}, status=status.HTTP_400_BAD_REQUEST)
