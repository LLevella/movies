import redis
from django.conf import settings
import psycopg2
from psycopg2 import sql
from django_rq import job


def request_to_obj(request, keys):
    obj = {}
    for key in keys:
        obj[key] = request.data.get(key)
    return obj


def one_from_many_keys(keys, separator):
    if len(keys) > 0:
        return separator.join(keys)
    return None


redis_movie_player_db = redis.StrictRedis(host=settings.REDIS_HOST,
                                          port=settings.REDIS_PORT, db=settings.MOVIEPLAYER_DB)
