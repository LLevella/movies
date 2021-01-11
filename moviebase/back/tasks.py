# from .models import MoviePlayer
# from .serializers import MoviePlayerSerializer
# from .views import movie_user_pointer
from django.conf import settings
import redis
import psycopg2

rdb = redis.StrictRedis(host=settings.REDIS_HOST,
                        port=settings.REDIS_PORT, db=settings.MOVIEPLAYER_DB)


pgdb = psycopg2.connect(dbname=settings.PG_DB_NAME, user=settings.PG_DB_USER,
                        password=settings.PG_DB_PASSWORD, host=settings.PG_DB_HOST)


def db_relocator():
    print("hi")
#     # for key_id in movie_user_pointer.scan_iter():
#     #     movie_str, user_str = key_id.split(":")
#     #     movie_id, user_id = int(movie_str), int(user_str)
#     #     new_pointer = movie_user_pointer.get(key_id)
#     #     if MoviePlayer.objects.filter(movie=movie_id, user=user_id).exists():
#     #         player = MoviePlayer.objects.get(movie=movie_id, user=user_id)
#     #         serializer = MoviePlayerSerializer(
#     #             player, pointer=new_pointr, partial=true)
#     #     else:
#     #         serializer = MoviePlayerSerializer(
#     #             movie=movie_id, user=user_id, pointer=new_pointer)
#     #     if serializer.is_valid():
#     #         serializer.save()
