from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import Movie, MoviePlayer
from .serializers import MovieListSerializer, MovieDetailSerializer,  MoviePlayerSerializer

from django.conf import settings
import redis

movie_user_pointer = redis.StrictRedis(host=settings.REDIS_HOST,
                                       port=settings.REDIS_PORT, db=settings.MOVIEPLAYER_REDIS)


class MovieListView(APIView):
    """Вывод списка фильмов"""

    def get(self, request):
        movies = Movie.objects.filter(draft=False)
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)


class MovieDetailView(APIView):
    """Вывод фильма"""

    def get(self, request, pk):
        movie = Movie.objects.get(id=pk, draft=False)
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data)


class MoviePlayerView(APIView):
    """Добавление времени, обновление, получение времени по фильму и пользователю """

    def post(self, request):
        serializer = MoviePlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            key_id = f'{movie_id}:{user_id}'
            pointer = serializer.data["pointer"]
            movie_user_pointer.set(key_id, pointer)
            return Response({"movie": movie_id, "user": user_id, "pointer": serializer.data['pointer']}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        movie_id = request.data.get("movie")
        user_id = request.data.get("user")
        key_id = f'{movie_id}:{user_id}'
        pointer = movie_user_pointer.get(key_id)
        if pointer:
            return Response({"movie": movie_id, "user": user_id, "pointer": pointer}, status=status.HTTP_200_OK)
        if MoviePlayer.objects.filter(movie=movie_id, user=user_id).exists():
            player = MoviePlayer.objects.get(movie=movie_id, user=user_id)
            serializer = MoviePlayerSerializer(player)
            return Response({"movie": movie_id, "user": user_id, "pointer": serializer.data['pointer']}, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def patch(self, request):
        movie_id = request.data.get("movie")
        user_id = request.data.get("user")
        new_pointer = request.data.get("pointer")
        key_id = f'{movie_id}:{user_id}'
        old_pointer = movie_user_pointer.get(key_id)
        if old_pointer:
            movie_user_pointer.set(key_id, new_pointer)
            return Response({"movie": movie_id, "user": user_id, "pointer": new_pointer}, status=status.HTTP_200_OK)
        if MoviePlayer.objects.filter(movie=movie_id, user=user_id).exists():
            movie_user_pointer.set(key_id, new_pointer)
            return Response({"movie": movie_id, "user": user_id, "pointer": new_pointer}, status=status.HTTP_200_OK)
        return Response({"errors": "Movies player is not found"}, status=status.HTTP_400_BAD_REQUEST)
