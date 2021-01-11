# from moviebase.celery import app

# from .models import MoviePlayer
# from .serializers import MoviePlayerSerializer
# from .views import movie_user_pointer

# from django.conf import settings
# import redis


# @app.task
# def db_relocator():
#     print("hi")
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

# from celery.task import periodic_task
# from datetime import timedelta


# @periodic_task(run_every=timedelta(seconds=60))
# def test():
#     print "is works!"
