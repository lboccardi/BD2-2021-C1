from pymongo import MongoClient
import time
import pprint

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


def findRandomRestaurant(db):
    collection = db['restaurants']

    start_time = time.time()
    x = collection.aggregate([{ "$sample": { "size": 1 } }])
    x = list(x)[0]
    print("Restaurant:\n")
    pprint.pprint(x)
    print("Execution query time:", time.time() - start_time)
    return x


def findRandomState(db):
    collection = db['states']

    start_time = time.time()
    x = collection.aggregate([{ "$sample": { "size": 1 } }])
    x = list(x)[0]
    print("State:\n")
    pprint.pprint(x)
    print("Execution query time:", time.time() - start_time)
    return x


def findNearestCompetitor(db,restaurant):
    collection = db['restaurants']

    start_time = time.time()
    x = collection.aggregate([
           { "$geoNear": {
               "near": restaurant['geometry'],
               "spherical": True,
               "query":{"properties.name": {'$ne':restaurant['properties']['name']}},
               "distanceField": "distance",
           }},{
           "$project":{'properties.name':1,'properties.address':1,"distance":1}
           },{
           "$limit":1
           }])
    print("\n\nNearest competitor:")
    pprint.pprint(list(x)[0])
    print("Execution query time:", time.time() - start_time)    


def findRestaurantsInState(db,state):
    collection = db['restaurants']

    start_time = time.time()
    x = list(collection.aggregate([{ 
            "$match": {
                'geometry':{
                    '$geoWithin': {'$geometry': state['geometry']}
                }
              }
        },
            {"$project":{'properties.name':1,'properties.address':1}}
    ]))
    print("\n\nRestaurants in: ",state['properties']['name'],len(x))
    pprint.pprint(x)
    print("Execution query time:", time.time() - start_time)
    return x

def findFranchiseCountInState(db,state):
    collection = db['restaurants']

    start_time = time.time()
    x = list(collection.aggregate([{ 
            "$match": {
                'geometry':{
                    '$geoWithin': {'$geometry': state['geometry']}
                }
              }
        },
            {"$group" : {"_id":"$properties.name", "count":{"$sum":1}}},
    ]))
    print("\n\nRestaurants by franchise in: ",state['properties']['name'])
    pprint.pprint(x)
    print("Execution query time:", time.time() - start_time)
    return x


if __name__ == '__main__':
    uri = "mongodb://{}:{}@{}:{}".format(MG_USER, MG_PASSWORD, IP_ADDRESS, PORT)

    db = connect_to_mongo(uri, DB_NAME)
    #collection = db['restaurants']

    #start_time = time.time()
    #result = restaurants_by_radius(collection, {"type": "Point", "coordinates": [-74.89021, 44.9213]}, 5000)
    #print(list(result))
    #print("Execution query time:", time.time() - start_time)
    
    
    ######################

    #random_restaurant = findRandomRestaurant(db)
    #findNearestCompetitor(db,random_restaurant)

    #random_state = findRandomState(db)
    #findRestaurantsInState(db,random_state)

    #findFranchiseCountInState(db,random_state)