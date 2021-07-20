import psycopg2
from psycopg2.extras import RealDictCursor
import time,os

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
        file_name = f"pg_output_{os.getpid()}.txt"
        self.file = open(file_name, 'w')

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

    def findRandomCounty(self):
        self.cur.execute("select * from counties order by random() limit 1")
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
        self.cur.execute(f"select name,address from restaurants where st_within(ST_SetSRID(geom, 4326),'{state['boundaries']}'::geometry)")
        total_time = time.time() - start_time    
        result = self.cur.fetchall()
        print("Restaurants in",state['name'],len(result),file=self.file)
        for r in result:
            print(r['name'],'-',r['address'],file=self.file)
        self.file.write("\n")
        return total_time


    def findFranchiseCountInState(self,state):
        start_time = time.time()
        self.cur.execute(f"select name,count(*) from restaurants where st_within(ST_SetSRID(geom, 4326),'{state['boundaries']}'::geometry) group by name")
        total_time = time.time() - start_time    
        result = self.cur.fetchall()
        print("Restaurants by franchise in",state['name'],file=self.file)
        for r in result:
            print(r['name'],'-',r['count'],file=self.file)
        self.file.write("\n")
        return total_time


    def find_counties_by_restaurant(self, restaurant):
        start_time = time.time()
        self.cur.execute(f"select name from counties where st_contains(boundaries, ST_SetSRID('{restaurant['geom']}'::geometry, 4326))")
        total_time = time.time() - start_time
        result = self.cur.fetchone()
        if result:
            print("Restaurant",restaurant['name'],"-",restaurant['address'],"is in county:",result['name'],file=self.file)
        else:
            print("Restaurant",restaurant['name'],"-",restaurant['address'],"is in county: - ",file=self.file)
        self.file.write("\n")
        return total_time

    def franchises_by_county(self, county):
        start_time = time.time()
        self.cur.execute(f"select count(distinct name) as franchises from restaurants where st_contains(st_polyfromtext('{county['wkt']}'), geom)")
        total_time = time.time() - start_time
        result = self.cur.fetchone()
        print("County",county['name']," has ",result['franchises'],"distinct franchises",file=self.file)
        self.file.write("\n")
        return total_time

    def writeIterationNum(self,i):
        print("Iteration",i,":\n",file=self.file)


