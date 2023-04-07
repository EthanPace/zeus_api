from json import loads
import pymongo

# Stations:
# 		- Tasks:
# 			- Insert a new weather station (single)
# 			- Update a specific weather station longitude and latitude (single)			
# 		- Methods: 			
# 			- Post:			
# 				- Input JSON: {new weather station}
# 				- Output JSON: {success / fail}	
# 			- PATCH:
# 				- Input JSON: {weather station & new values}
# 				- Output JSON: {success / fail}
# 		- Triggers:
# 			- If there are not enough weather station per state, add dummy data		 

client = pymongo.MongoClient("mongodb+srv://testUser:testPassword@nasadata.dpq7x0s.mongodb.net/test")
db = client['weatherDataDB']
coll = db['stations']

def station(json_object):
    new_record = {}
    for key in json_object:
        new_record[key] = json_object[key]
    return new_record

def find(limit):
    return coll.find().limit(int(limit))

def create(new):
    return coll.insert_one(station(new))

def update(search_terms, new):
    return coll.update_one(search_terms, new)

def delete(search_terms):
    return coll.delete_one(search_terms)