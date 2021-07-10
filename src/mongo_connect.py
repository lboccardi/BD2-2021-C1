import collections
from pymongo import MongoClient
import time
import pprint

DB_NAME = 'bd2'
IP_ADDRESS = '52.72.181.125'
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
    result= collection.aggregate([{ "$sample": { "size": 1 } }])
    print("\nExecution query time:", time.time() - start_time)
    result= list(result)[0]
    print("Restaurant:")
    print(result['properties']['name'],'-',result['properties']['address'])
    return result


def findRandomState(db):
    collection = db['states']

    start_time = time.time()
    result= collection.aggregate([{ "$sample": { "size": 1 } }])
    print("\nExecution query time:", time.time() - start_time)
    result= list(result)[0]
    print("State:")
    print(result['properties']['name'])
    return result


def findNearestCompetitor(db,restaurant):
    collection = db['restaurants']

    start_time = time.time()
    result= collection.aggregate([
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
    print("\nExecution query time:", time.time() - start_time)
    result= list(result)[0]    
    print("Nearest competitor:")
    pprint.pprint(result)
    return result


def findRestaurantsInState(db,state):
    collection = db['restaurants']

    start_time = time.time()
    result= collection.aggregate([{ 
            "$match": {
                'geometry':{
                    '$geoWithin': {'$geometry': state['geometry']}
                }
              }
        },
            {"$project":{'properties.name':1,'properties.address':1}}
    ])
    print("\nExecution query time:", time.time() - start_time)
    result= list(result)
    print("Restaurants in: ",state['properties']['name'],len(result))
    for r in result:
        print(r['properties']['name'],'-',r['properties']['address'])
    return result

def findFranchiseCountInState(db,state):
    collection = db['restaurants']

    start_time = time.time()
    result= collection.aggregate([{ 
            "$match": {
                'geometry':{
                    '$geoWithin': {'$geometry': state['geometry']}
                }
              }
        },
            {"$group" : {"_id":"$properties.name", "count":{"$sum":1}}},
    ])
    print("\nExecution query time:", time.time() - start_time)
    result= list(result)
    print("Restaurants by franchise in: ",state['properties']['name'])
    for r in result:
        print(r['_id'],'-',r['count'])
    return result

def find_state_by_restaurant(db, restaurant):
    collection = db['states']
    result = collection.find({
        'geometry': {
            '$geoIntersects': {
                '$geometry': restaurant['geometry']
            }
        }
    })
    return result

def franchises_by_state(db, state):
    collection = db['restaurants']
    return collection.aggregate([
        {
            '$match': {
                'geometry': {
                    '$geoWithin': {'$geometry': state['geometry']}
                }
            }
        },
        {
            '$group': {'_id': "$properties.name", 'total': {'$sum': 1}}
        },
        {
            '$count': "franchises"
        }
    ])

if __name__ == '__main__':
    uri = "mongodb://{}:{}@{}:{}".format(MG_USER, MG_PASSWORD, IP_ADDRESS, PORT)
    # uri = "mongodb://localhost:27017/academica"

    db = connect_to_mongo(uri, DB_NAME)
    #collection = db['restaurants']

    random_restaurant = findRandomRestaurant(db)
    start_time = time.time()
    #result = restaurants_by_radius(collection, {"type": "Point", "coordinates": [-74.89021, 44.9213]}, 5000)
    result = find_state_by_restaurant(db, random_restaurant)
    print("Execution query time:", time.time() - start_time)
    print(f"state: {list(result)[0]['properties']['name']}")
    
    
    
    ######################

    # random_restaurant = findRandomRestaurant(db)
    # findNearestCompetitor(db,random_restaurant)

    # random_state = findRandomState(db)
    #findRestaurantsInState(db,random_state)
    # findFranchiseCountInState(db,random_state)