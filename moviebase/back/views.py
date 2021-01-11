from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import Movie, MoviePlayer
from .serializers import MovieListSerializer, MovieDetailSerializer,  MoviePlayerSerializer

from django.conf import settings
import redis

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                  port=settings.REDIS_PORT, db=0)

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
            player_id = serializer.data["id"]
            pointer = serializer.data["pointer"]
            redis_instance.set(player_id, pointer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        movie_id = request.data.get("movie")
        user_id = request.data.get("user")
        if MoviePlayer.objects.filter(movie=movie_id, user=user_id).exists():
            player = MoviePlayer.objects.get(movie=movie_id, user=user_id)
            serializer = MoviePlayerSerializer(player)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, format=None):
        player_id = request.data.get("id")
        new_pointer = request.data.get("pointer")
        old_pointer = redis_instance.get(player_id)
        if old_pointer:
            redis_instance.set(player_id, new_pointer)
            return Response({"id": player_id, "pointer": new_pointer}, status=status.HTTP_200_OK)
        return Response({"errors": "player id is not found"}, status=status.HTTP_400_BAD_REQUEST)
        # player = MoviePlayer.objects.get(id=request.data.get("id"))   
        # serializer = MoviePlayerSerializer(player, data=request.data, partial=True)
        # if serializer.is_valid():            
        #     serializer.save()           
        #     return Response(serializer.data, status=status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
