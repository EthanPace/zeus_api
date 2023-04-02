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
    new_record = {
        'Device ID': json_object['Device ID'],
        'Device Name': json_object['Device Name'],
        'Latitude': json_object['Latitude'],
        'Longitude': json_object['Longitude'],
    }
    return new_record

def find(limit):
    return coll.find().limit(int(limit))
    
def search(search_terms):
    return coll.find_one(search_terms)

def create(new):
    return coll.insert_one(station(new))

def update(search_terms, new):
    return coll.update_one(search_terms, new)

def delete(search_terms):
    return coll.delete_one(search_terms)