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


if __name__ == '__main__':
    uri = "mongodb://{}:{}@{}:{}".format(MG_USER, MG_PASSWORD, IP_ADDRESS, PORT)

    db = connect_to_mongo(uri, DB_NAME)
    collection = db['states']

    start_time = time.time()
    print(collection.find_one())
    print("Execution query time:", time.time() - start_time)
