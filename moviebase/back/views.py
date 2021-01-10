from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import Movie, MoviePlayer
from .serializers import MovieListSerializer, MovieDetailSerializer,  MoviePlayerSerializer


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
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, movie_id, user_id):
        player = MoviePlayer.objects.get(movie=movie_id, user=user_id)
        serializer = MoviePlayerSerializer(player)
        return Response(serializer.data)

    def put(self, request, format=None):
        print("id====", request.data.get("id"))
        player = MoviePlayer.objects.get(id=request.data.get("id"))   
        serializer = MoviePlayerSerializer(player, data=request.data)
        if serializer.is_valid():            
            serializer.save()           
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
