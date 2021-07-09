import psycopg2
from psycopg2.extras import RealDictCursor
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

def findRandomRestaurant(cursor):
    start_time = time.time()
    cursor.execute("select * from restaurants where random() < 1000 limit 1")
    print("\nExecution query time:", time.time() - start_time)    
    result = cursor.fetchone()
    print("Restaurant:")
    print(result['name'],'-',result['address'])
    return result


def findRandomState(cursor):
    start_time = time.time()
    cursor.execute("select * from states where random() < 1000 limit 1")
    print("\nExecution query time:", time.time() - start_time)    
    result = cursor.fetchone()
    print("State:")
    print(result['name'])
    return result


def findNearestCompetitor(cursor,restaurant):
    start_time = time.time()
    cursor.execute(f"select name,address, st_distance(geom::geography, st_makepoint({restaurant['longitude']},{restaurant['latitude']})::geography) as distance from restaurants where name!= %s order by distance limit 1",(restaurant['name'],))
    print("\nExecution query time:", time.time() - start_time)    
    result = cursor.fetchone()
    print("Nearest competitor:")
    print(result)
    return result

def findRestaurantsInState(cursor,state):
    start_time = time.time()
    cursor.execute(f"select name,address from restaurants where st_within(geom,st_geomfromtext('{state['wkt']}'))")
    print("\nExecution query time:", time.time() - start_time)    
    result = cursor.fetchall()
    print("Restaurants in",state['name'],len(result))
    for r in result:
        print(r['name'],'-',r['address'])
    return result


def findFranchiseCountInState(cursor,state):
    start_time = time.time()
    cursor.execute(f"select name,count(*) from restaurants where st_within(geom,st_geomfromtext('{state['wkt']}')) group by name")
    print("\nExecution query time:", time.time() - start_time)    
    result = cursor.fetchall()
    print("Restaurants by franchise in",state['name'])
    for r in result:
        print(r['name'],'-',r['count'])
    return result


if __name__ == '__main__':

    conn = connect_to_postgres(DB_NAME, PG_USER, PG_PASSWORD, IP_ADDRESS, PORT)
    cur = conn.cursor(cursor_factory=RealDictCursor)

    start_time = time.time()

    # cur.execute(f"SELECT * FROM STATES")
    #result = restaurants_by_radius(cur, "-74.89021, 44.9213", 5000)

    #print("Execution query time:", time.time() - start_time)
    #print(list(result))

    # for i in cur.fetchall():
    #     print(i[1])

    #random_restaurant = findRandomRestaurant(cur)
    #findNearestCompetitor(cur,random_restaurant)

    #random_state = findRandomState(cur)
    #findRestaurantsInState(cur,random_state)
    #findFranchiseCountInState(cur,random_state)
    cur.close()
    conn.close()

