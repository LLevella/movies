from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView

from .models import Movie, MoviePlayer
from .serializers import MovieListSerializer, MovieDetailSerializer,  MoviePlayerSerializer
from .service import redis_movie_player_db, one_from_many_keys, request_to_obj


class MovieListView(APIView):
    """Вывод списка фильмов"""

    def get(self, request):
        movies = Movie.objects.filter(draft=False)
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MovieDetailView(APIView):
    """Вывод фильма"""

    def get(self, request):
        if Movie.objects.filter(id=request.data.get("movie"), draft=False).exists():
            movie = Movie.objects.get(
                id=request.data.get("movie"), draft=False)
            serializer = MovieDetailSerializer(movie)
            obj = dict(serializer.data)
            if not request.user.is_authenticated:
                # отправим на страницу входа
                obj["film"] = f"/auth/token/login"
            return Response(obj, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class MoviePlayerView(APIView):
    """Добавление времени, обновление, получение времени по фильму и пользователю """
    # в данном случае мы можем коротко запретить доступ не авторизованным
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        for key in redis_movie_player_db.scan_iter("*"):
            print(key.decode('utf-8'))
            pointer = redis_movie_player_db.get(key.decode('utf-8'))
            print(key.decode('utf-8'), pointer.decode('utf-8'))
            pointer = redis_movie_player_db.get(key)
            print(key, pointer)
            print("======================")
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
