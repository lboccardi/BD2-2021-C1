import psycopg2
import time

DB_NAME = 'bd2'
IP_ADDRESS = 'postgres-bd.c3amsvppfcze.us-east-1.rds.amazonaws.com'
PORT = 5432

try:
    from credentials import *
except ImportError:
    pass


def connect_to_postgres(dbname, user, password, host, port):
    return psycopg2.connect(dbname=dbname, user=user, password=password,
                            host=host, port=port)

def restaurants_by_radius(cursor, person, radius):
    cursor.execute(f"select *, st_distance(geom::geography, st_makepoint({person})::geography) as distance from restaurants where st_distance(geom::geography, st_makepoint({person})::geography) < {radius}")
    return cursor.fetchall()

if __name__ == '__main__':

    conn = connect_to_postgres(DB_NAME, PG_USER, PG_PASSWORD, IP_ADDRESS, PORT)
    cur = conn.cursor()

    start_time = time.time()

    # cur.execute(f"SELECT * FROM STATES")
    result = restaurants_by_radius(cur, "-74.89021, 44.9213", 5000)

    print("Execution query time:", time.time() - start_time)
    print(list(result))

    # for i in cur.fetchall():
    #     print(i[1])

    cur.close()
    conn.close()

