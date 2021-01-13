from django.conf import settings
from django_rq import job
import datetime
import redis
import psycopg2
from psycopg2 import sql

def r_delete_keys(rdb, keys):
    for key in keys:
        rdb.delete(key)


def pg_exist(pgdb, table, condition):
    with pgdb.cursor() as cursor:
        sql_select = f'select exists(select 1 from {table} where {condition})'
        qexist = sql.SQL(sql_select)
        cursor.execute(qexist)
        row = cursor.fetchone()
    return row[0]


def pg_insert_or_update(pgdb, table, values):
    with pgdb.cursor() as cursor:
        pgdb.autocommit = True
        for value in values:
            print("value = ", value)
            try:
                condition = f"movie_id = {value[0]} and user_id = {value[1]}"
                if pg_exist(pgdb, table, condition):
                    sql_query = f'UPDATE {table} SET pointer = {value[2]} WHERE {condition} '
                else:
                    if (pg_exist(pgdb, 'auth_user', f'id={value[1]}') and pg_exist(pgdb, 'back_movie', f'id={value[0]}')):
                        sql_query = f'INSERT INTO {table} (movie_id, user_id, pointer) VALUES ({value[0]}, {value[1]}, {value[2]})'
                cursor.execute(sql_query)
            except psycopg2.IntegrityError as e:
                print(e.pgcode)
                return False
    return True


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
        print("key =", key_id)
        movie_id, user_id = key_id.decode('utf-8').split(":")
        pointer = rdb.get(key_id)
        if cur_i == counter:
            if pg_insert_or_update(pgdb, 'back_movieplayer', pgdb_values):
                r_delete_keys(rdb, rdb_keys)
            else:
                print("Problems was with the same data: ")
                print(pgdb_values, rdb_keys)
            cur_i = 0
            pgdb_values.clear()
            rdb_keys.clear()
        else:
            pgdb_values.append(
                (int(movie_id), int(user_id), int(pointer.decode('utf-8'))))
            rdb_keys.append(key_id)
            cur_i = cur_i + 1

    if cur_i > 0:
        if pg_insert_or_update(pgdb, 'back_movieplayer', pgdb_values):
            r_delete_keys(rdb, rdb_keys)
        else:
            print("Problems was with the same data: ")
            print(pgdb_values, rdb_keys)

    pgdb.close()


def r_db_clean(rdb, pgdb, table):
    clean_keys = []
    delta = datetime.timedelta(30)  # 30 дней будут  жить id
    today = datetime.datetime.now(datetime.timezone.utc)

    for key in rdb.scan_iter():
        key_id = int(key.decode('utf-8'))
        condition = f"id = {key_id}"
        if not pg_exist(pgdb, table, condition):
            clean_keys.append(key)
        value = rdb.get(key)
        last_active_date = datetime.datetime.strptime(
            value.decode('utf-8'), '%Y-%m-%d %H:%M:%S')
        if last_active_date < (today - delta):
            clean_keys.append(key)

    r_delete_keys(rdb, clean_keys)


@job
def r_tmp_storage_clean():
    rdb_movies = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT, db=settings.MOVIES_DB)
    rdb_users = redis.StrictRedis(host=settings.REDIS_HOST,
                                  port=settings.REDIS_PORT, db=settings.USERS_DB)
    pgdb = psycopg2.connect(dbname=settings.PG_DB_NAME, user=settings.PG_DB_USER,
                            password=settings.PG_DB_PASSWORD, host=settings.PG_DB_HOST)
    r_db_clean(rdb_users, pgdb, "auth_user")
    r_db_clean(rdb_movies, pgdb, "back_movie")
