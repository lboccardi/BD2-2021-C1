import psycopg2
from psycopg2.extras import RealDictCursor
import time

DB_NAME = 'bd2'
IP_ADDRESS = 'postgres-bd.c3amsvppfcze.us-east-1.rds.amazonaws.com'
PORT = 5432
# DB_NAME = 'postgres'
# IP_ADDRESS = '127.0.0.1'
# PORT = 5433

try:
    from credentials import *
except ImportError:
    pass

def connect_to_postgres(dbname, user, password, host, port):
    return psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

class Postgis:

    def __init__(self, dbname, user, password, host, port):
        conn = connect_to_postgres(dbname, user, password, host, port)
        self.cur = conn.cursor(cursor_factory=RealDictCursor)
        self.file = open('pg_output.txt', 'w')

    def restaurants_by_radius(self, person, radius):
        start_time = time.time()
        self.cur.execute(f"select *, st_distance(geom::geography, '{person['location']}'::geography) as distance from restaurants where st_distance(geom::geography, '{person['location']}'::geography) < {radius}")
        total_time = time.time() - start_time
        result = self.cur.fetchall()
        self.file.write(f"Restaurants by radius:\n\tPerson: {person['name']} [{person['longitude']},{person['latitude']}] - Radius: {radius}\n")        
        for r in result:
            print(r['name'],'-',r['address'],'-',r['distance'],file=self.file)   
        self.file.write("\n") 
        return total_time

    def findRandomRestaurant(self):
        self.cur.execute("select * from restaurants order by random() limit 1")
        return self.cur.fetchone()


    def findRandomState(self):
        self.cur.execute("select * from states order by random() limit 1")
        return self.cur.fetchone()

    def findRandomCustomer(self):
        self.cur.execute("select * from customers order by random() limit 1")   
        return self.cur.fetchone()


    def findNearestCompetitor(self,restaurant):
        start_time = time.time()
        self.cur.execute(f"select name,address, st_distance(geom::geography,'{restaurant['geom']}'::geometry::geography) as distance from restaurants where name!= %s order by distance limit 1",(restaurant['name'],))
        total_time = time.time() - start_time    
        r = self.cur.fetchone()
        print("Nearest competitor of",restaurant['name'],'-',restaurant['address'],file=self.file)
        print(r['name'],'-',r['address'],'-',r['distance'],file=self.file)
        self.file.write("\n")
        return total_time

    def findRestaurantsInState(self,state):
        start_time = time.time()
        self.cur.execute(f"select name,address from restaurants where st_within(geom,st_geomfromtext('{state['wkt']}'))")
        total_time = time.time() - start_time    
        result = self.cur.fetchall()
        print("Restaurants in",state['name'],len(result),file=self.file)
        for r in result:
            print(r['name'],'-',r['address'],file=self.file)
        self.file.write("\n")
        return total_time


    def findFranchiseCountInState(self,state):
        start_time = time.time()
        self.cur.execute(f"select name,count(*) from restaurants where st_within(geom,st_geomfromtext('{state['wkt']}')) group by name")
        total_time = time.time() - start_time    
        result = self.cur.fetchall()
        print("Restaurants by franchise in",state['name'],file=self.file)
        for r in result:
            print(r['name'],'-',r['count'],file=self.file)
        self.file.write("\n")
        return total_time


    def find_counties_by_restaurant(self, restaurant):
        start_time = time.time()
        self.cur.execute(f"select name from counties where st_contains(wkt, '{restaurant['geom']}')")
        total_time = time.time() - start_time
        result = self.cur.fetchone()
        if result:
            print("Restaurant",restaurant['name'],"-",restaurant['address'],"is in county:",result['name'],file=self.file)
        else:
            print("Restaurant",restaurant['name'],"-",restaurant['address'],"is in county: - ",file=self.file)
        self.file.write("\n")
        return total_time

    def franchises_by_state(self, state):
        start_time = time.time()
        self.cur.execute(f"select count(distinct name) as franchises from restaurants where st_contains(st_polyfromtext('{state['wkt']}'), geom)")
        total_time = time.time() - start_time
        result = self.cur.fetchone()
        print("State",state['name']," has ",result['franchises'],"distinct franchises",file=self.file)
        self.file.write("\n")
        return total_time

    def writeIterationNum(self,i):
        print("Iteration",i,":\n",file=self.file)

# if __name__ == '__main__':

#     conn = connect_to_postgres(DB_NAME, PG_USER, PG_PASSWORD, IP_ADDRESS, PORT)
#     cur = conn.cursor(cursor_factory=RealDictCursor)

#     rest = findRandomRestaurant(cur)

#     start_time = time.time()

#     result = find_state_by_restaurant(cur, dict(rest))

#     # cur.execute(f"SELECT * FROM STATES")
#     result = restaurants_by_radius(cur, "-74.89021, 44.9213", 5000)

#     #print("Execution query time:", time.time() - start_time)
#     #print(dict(result[0]))

#     # for i in cur.fetchall():
#     #     print(i[1])

#     #random_restaurant = findRandomRestaurant(cur)
#     #findNearestCompetitor(cur,random_restaurant)

#     #random_state = findRandomState(cur)
#     #findRestaurantsInState(cur,random_state)
#     #findFranchiseCountInState(cur,random_state)
#     cur.close()
#     conn.close()

