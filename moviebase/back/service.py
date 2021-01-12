import redis
from django.conf import settings


def request_to_obj(request, keys):
    obj = {}
    for key in keys:
        obj[key] = request.data.get(key)
    return obj


def one_from_many_keys(keys, separator):
    return separator.join(keys)


redis_movie_player_db = redis.StrictRedis(host=settings.REDIS_HOST,
                                          port=settings.REDIS_PORT, db=settings.MOVIEPLAYER_DB)
