from src.mongo_connect import MongoDB
from src.postgres_connect import Postgis
import sys, time, os
import pandas as pd
import numpy as np

MONGO_DB_NAME = 'bd2'
MONGO_IP_ADDRESS = '52.72.181.125'
MONGO_PORT = 27017

PG_DB_NAME = 'bd2'
PG_IP_ADDRESS = 'postgres-bd.c3amsvppfcze.us-east-1.rds.amazonaws.com'
PG_PORT = 5432

ITERATIONS = int(sys.argv[1])
FORKS = int(sys.argv[2])
DECIMALS = int(sys.argv[3])

try:
    from src.credentials import *
except ImportError:
    pass

i = 0
for i in range(FORKS-1):
    pid = os.fork()
    if (pid == 0):
        break

print("Process ID:", os.getpid())

uri = "mongodb://{}:{}@{}:{}".format(MG_USER, MG_PASSWORD, MONGO_IP_ADDRESS, MONGO_PORT)
mongo = MongoDB(uri, MONGO_DB_NAME)
pg = Postgis(PG_DB_NAME, PG_USER, PG_PASSWORD, PG_IP_ADDRESS, PG_PORT)

times_labels=["Find County by a restaurant","Find nearest competitor from a restaurant","Find Restaurant by costumer","Find restaurant per franchise in State","Find all the restaurants in a State","Find count of distinct franchises on State"]
mongo_times=[0,0,0,0,0,0]
postgres_times=[0,0,0,0,0,0]

start_time = time.time()
for i in range(ITERATIONS):
    #### MONGO ####
    mongo.writeIterationNum(i)
    r = mongo.findRandomRestaurant()
    mongo_times[0] += mongo.find_county_by_restaurant(r)
    mongo_times[1] += mongo.findNearestCompetitor(r)
    c = mongo.findRandomCustomer()
    mongo_times[2] += mongo.restaurants_by_radius(c, 50000)

    t = mongo.findRandomCounty()
    mongo_times[5] += mongo.franchises_by_county(t)

    s = mongo.findRandomState()
    mongo_times[3] += mongo.findFranchiseCountInState(s)
    mongo_times[4] += mongo.findRestaurantsInState(s)

    ###Postgres"
    pg.writeIterationNum(i)
    r = pg.findRandomRestaurant()
    postgres_times[0] += pg.find_counties_by_restaurant(r)
    postgres_times[1] += pg.findNearestCompetitor(r)
    c = pg.findRandomCustomer()
    postgres_times[2] += pg.restaurants_by_radius(c, 50000)
    
    t = pg.findRandomCounty()
    postgres_times[5] += pg.franchises_by_county(t)

    s = pg.findRandomState()
    postgres_times[3] += pg.findFranchiseCountInState(s)
    postgres_times[4] += pg.findRestaurantsInState(s)

total_time = time.time() - start_time    
print(os.getpid(),"- Iterations:",ITERATIONS,"- Total time:",round(total_time,5),"\n\n")
for i in range(len(mongo_times)):
    print(times_labels[i],":")
    print("\tMongo:")
    print("\t\ttotal:",round(mongo_times[i], DECIMALS))
    print("\t\taverage:",round(mongo_times[i]/ITERATIONS, DECIMALS))
    print("\tPostgres:")
    print("\t\ttotal:",round(postgres_times[i], DECIMALS))
    print("\t\taverage:",round(postgres_times[i]/ITERATIONS, DECIMALS))
    
# file_name = f"results_{os.getpid()}.csv"
# mongo_times_prom=[0,0,0,0,0,0]
# postgres_times_prom=[0,0,0,0,0,0]
# for i in range(6):
#     mongo_times_prom[i]=mongo_times[i]/ITERATIONS
#     postgres_times_prom[i]=postgres_times[i]/ITERATIONS

# result = np.array([mongo_times,mongo_times_prom,postgres_times,postgres_times_prom])
# result = result.T

# df=pd.DataFrame(result,columns=['mongo total','mongo promedio','postgres total','postgres promedio'])
# df.to_csv(file_name)

