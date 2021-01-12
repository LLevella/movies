from django.conf import settings
import redis
import psycopg2
from django_rq import job


def pg_insert_or_update(pgdb, values):
    with pgdb.cursor() as cursor:
        pgdb.autocommit = True
        print("commit")
        insert = sql.SQL('INSERT INTO back_movieplayer (movie_id, user_id, pointer) VALUES {}').format(
            sql.SQL(',').join(map(sql.Literal, values))
        )
    cursor.execute(insert)


def r_delete_keys(rdb, keys):
    for key in keys:
        rdb.delete(key)


@job
def db_relocator():
    counter = 50
    rdb = redis.StrictRedis(host=settings.REDIS_HOST,
                            port=settings.REDIS_PORT, db=settings.MOVIEPLAYER_DB)

    pgdb = psycopg2.connect(dbname=settings.PG_DB_NAME, user=settings.PG_DB_USER,
                            password=settings.PG_DB_PASSWORD, host=settings.PG_DB_HOST)
    cur_i = 0
    pgdb_values = list()
    rdb_keys = list()

    for key_id in rdb.scan_iter():
        movie_id, user_id = key_id.decode('utf-8').split(":")
        pointer = rdb.get(key_id)
        if cur_i == counter:
            pg_insert_or_update(pgdb, pgdb_values)
            r_delete_keys(rdb, rdb_keys)
            cur_i = 0
            pgdb_values.clear()
            rdb_keys.clear()
        else:
            pgdb_values.append(
                (int(movie_id), int(user_id), int(pointer.decode('utf-8'))))
            cur_i = cur_i + 1

    if cur_i > 0:
        pg_insert_or_update(pgdb, pgdb_values)
        r_delete_keys(rdb, rdb_keys)

    pgdb.close()
