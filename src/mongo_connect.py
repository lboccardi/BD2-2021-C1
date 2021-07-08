from pymongo import MongoClient
import time

DB_NAME = 'bd2'
IP_ADDRESS = '34.201.242.58'
PORT = 27017


try:
    from credentials import *
except ImportError:
    pass


def connect_to_mongo(uri, db_name):
    return MongoClient(uri)[db_name]

def restaurants_by_radius(collection, person, radius):
    return collection.aggregate([
        {
        '$geoNear': {
            'near': person,
            'distanceField': "dist.calculated",
            'maxDistance': radius,
            'includeLocs': "dist.location",
            'spherical': True
            }
        }
    ])


if __name__ == '__main__':
    uri = "mongodb://{}:{}@{}:{}".format(MG_USER, MG_PASSWORD, IP_ADDRESS, PORT)

    db = connect_to_mongo(uri, DB_NAME)
    collection = db['restaurants']

    start_time = time.time()
    result = restaurants_by_radius(collection, {"type": "Point", "coordinates": [-74.89021, 44.9213]}, 5000)
    print(list(result))
    print("Execution query time:", time.time() - start_time)
