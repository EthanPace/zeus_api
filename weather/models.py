from json import loads
from bson.json_util import dumps
from bson.objectid import ObjectId
import pymongo

# Weather:
# 		- Tasks:
# 			- Insert new fields to record the temperature information in Fahrenheit (6 fields) (multiple) -- DONE
# 			- Find the temperature, atmospheric pressure, radiation and precipitation recorded by a specific station at a given date and time (hour) (multiple) -- TO DO (Can't get it to search, only to limit)
# 			- Create a query that includes an index key -- TO DO (No clue what this means)
# 		- Methods: 
# 			- PUT:
# 				- Input JSON: {6 different object ids} -- DONE
# 				- Output JSON {success / fail} -- DONE
# 			- GET:
# 				- Input JSON: {} -- DONE
# 				- Output JSON {Top 10 results} -- DONE
# 			    - For testing: localhost:8000/weather		
# 		
# 				- Input JSON: {Search terms} -- DONE
# 				- Output JSON {Result(s)} -- DONE
# 			    - For testing: localhost:8000/weather?time=Now&device_id=dlb_atm41_5282&limit=6

client = pymongo.MongoClient("mongodb+srv://testUser:testPassword@nasadata.dpq7x0s.mongodb.net/test")
db = client['weatherDataDB']
coll = db['NSWWeatherData']

def weather(json_object):
    new_record = {}
    for key in json_object:
        new_record[key] = json_object[key]
    return new_record

def find(search = "", limit = 10):
    if search == "":
        return coll.find().limit(limit)
    else:
        return coll.find({"_id":ObjectId(search)}).limit(limit)
    
def search(query):
    if 'time' in query and 'device_id' in query:
        time = query['time']
        device_id = query['device_id']
        return coll.find({"Time":time, "Device ID":device_id}).limit(int(query.get('limit', 10)))
    elif 'time' in query:
        time = query['time']
        return coll.find({"Time":time}).limit(int(query.get('limit', 10)))
    elif 'device_id' in query:
        device_id = query['device_id']
        return coll.find({"Device ID":device_id}).limit(int(query.get('limit', 10)))
        

def create(new):
    return coll.insert_one(weather(new))

def bulk_create(new_array):
    object_list = []
    for new in new_array:
        object_list += weather(new)
    return coll.insert_many(object_list)

def update(query, update):
    return coll.update_one(query, update)

def bulk_update(query, update, limit = None):
    if limit == None:
        return coll.update_many(query, update)
    else:
        try:
            cursor = coll.find(query).limit(limit)
            for document in cursor:
                coll.update_one({"_id":document["_id"]}, update)
            return {"results": "success"}
        except:
            return {"results": "fail"}

def delete(search_terms):
    return coll.delete_one(search_terms)

def bulk_delete(search_terms):
    return coll.delete_many(search_terms)
