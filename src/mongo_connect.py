import collections
from pymongo import MongoClient
import time
import pprint

def connect_to_mongo(uri, db_name):
    return MongoClient(uri)[db_name]

class MongoDB:

    def __init__(self, uri, db_name):
        self.db = connect_to_mongo(uri, db_name)
        self.file = open('mongo_output.txt', 'w')

    def restaurants_by_radius(self, person, radius):
        start_time = time.time()
        result = self.db['restaurants'].aggregate([
            {
            '$geoNear': {
                'near': person['geometry'],
                'distanceField': "dist.calculated",
                'maxDistance': radius,
                'spherical': True
                }
            }
        ])
        total_time = time.time() - start_time
        result= list(result)
        self.file.write(f"Restaurants by radius:\n\tPerson: {person['properties']['name']} {person['geometry']['coordinates']} - Radius: {radius}\n")
        for r in result:
            print(r['properties']['name'],'-',r['properties']['address'],'-',r['dist']['calculated'],file=self.file)
        self.file.write("\n")
        return total_time    
    
    def findRandomRestaurant(self):
        collection = self.db['restaurants']
        result= collection.aggregate([{ "$sample": { "size": 1 } }])
        result= list(result)[0]
        return result

    def findRandomState(self):
        collection = self.db['states']
        result= collection.aggregate([{ "$sample": { "size": 1 } }])
        result= list(result)[0]
        return result

    def findRandomCustomer(self):
        collection = self.db['customers']
        result= collection.aggregate([{ "$sample": { "size": 1 } }])
        result= list(result)[0]
        return result

    def findNearestCompetitor(self,restaurant):
        collection = self.db['restaurants']

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
        total_time = time.time() - start_time
        result= list(result)
        if result:
            result = result[0]    
        self.file.write("Nearest competitor of "+restaurant['properties']['name']+" - "+restaurant['properties']['address']+":\n")
        print(result['properties']['name'],'-',result['properties']['address'],'-',result['distance'],file=self.file)
        self.file.write("\n")
        return total_time

    def findRestaurantsInState(self,state):
        collection = self.db['restaurants']

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
        total_time = time.time() - start_time
        result= list(result)
        print("Restaurants in: ",state['properties']['name'],len(result),file=self.file)
        for r in result:
            print(r['properties']['name'],'-',r['properties']['address'],file=self.file)
        self.file.write("\n")
        return total_time

    def findFranchiseCountInState(self,state):
        collection = self.db['restaurants']

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
        total_time = time.time() - start_time
        result= list(result)
        print("Restaurants by franchise in: ",state['properties']['name'],file=self.file)
        for r in result:
            print(r['_id'],'-',r['count'],file=self.file)
        self.file.write("\n")
        return total_time

    def find_state_by_restaurant(self, restaurant):
        collection = self.db['states']
        start_time = time.time()
        result = collection.find({
            'geometry': {
                '$geoIntersects': {
                    '$geometry': restaurant['geometry']
                }
            }
        })
        total_time = time.time() - start_time
        result = list(result)
        if result:
            print("Restaurant",restaurant['properties']['name'],"-",restaurant['properties']['address'],"is in state:",result[0]['properties']['name'],file=self.file)
        else:
            print("Restaurant",restaurant['properties']['name'],"-",restaurant['properties']['address'],"is in state:","-",file=self.file)
        self.file.write("\n")
        return total_time

    def franchises_by_state(self, state):
        collection = self.db['restaurants']
        start_time = time.time()
        result = collection.aggregate([
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
        total_time = time.time() - start_time
        result = list(result)
        if result:
            print("State",state['properties']['name']," has ",result[0]['franchises'],"distinct franchises",file=self.file)
        else:
            print("State",state['properties']['name']," has 0 distinct franchises",file=self.file)
        self.file.write("\n")
        return total_time


    def writeIterationNum(self,i):
        print("Iteration",i,":\n",file=self.file)

# if __name__ == '__main__':
#     uri = "mongodb://{}:{}@{}:{}".format(MG_USER, MG_PASSWORD, IP_ADDRESS, PORT)
#     # uri = "mongodb://localhost:27017/academica"

#     db = connect_to_mongo(uri, DB_NAME)
#     #collection = db['restaurants']

#     random_restaurant = findRandomRestaurant(db)
#     start_time = time.time()
#     #result = restaurants_by_radius(collection, {"type": "Point", "coordinates": [-74.89021, 44.9213]}, 5000)
#     result = find_state_by_restaurant(db, random_restaurant)
#     print("Execution query time:", time.time() - start_time)
#     print(f"state: {list(result)[0]['properties']['name']}")
    
    
    
#     ######################

#     # random_restaurant = findRandomRestaurant(db)
#     # findNearestCompetitor(db,random_restaurant)

#     # random_state = findRandomState(db)
#     #findRestaurantsInState(db,random_state)
#     # findFranchiseCountInState(db,random_state)