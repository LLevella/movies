import redis
from django.conf import settings
import psycopg2
from psycopg2 import sql
from django_rq import job


redis_movie_player_db = redis.StrictRedis(host=settings.REDIS_HOST,
                                          port=settings.REDIS_PORT, db=settings.MOVIEPLAYER_DB)

redis_movies_db = redis.StrictRedis(host=settings.REDIS_HOST,
                                    port=settings.REDIS_PORT, db=settings.MOVIES_DB)
redis_users_db = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT, db=settings.USERS_DB)


def request_to_obj(request, keys):
    obj = {}
    for key in keys:
        obj[key] = request.data.get(key)
    return obj


def one_from_many_keys(keys, separator):
    if len(keys) > 0:
        return separator.join(keys)
    return None


def quick_check(rdb, key):
    if rdb.get(key):
        return True
    return False


def long_check(model, ***args, **kwargs):
    return model.objects.filter(**kwargs).exists()
