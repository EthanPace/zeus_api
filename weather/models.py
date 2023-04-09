from json import loads
from bson.json_util import dumps
from bson.objectid import ObjectId
import pymongo

# Weather:
# 		- Tasks:
# 			- Insert new fields to record the temperature information in Fahrenheit (6 fields) (multiple)
# 			- Find the temperature, atmospheric pressure, radiation and precipitation recorded by a specific station at a given date and time (hour) (multiple)
# 			- Create a query that includes an index key		
# 		- Methods: 
# 			- PUT:
# 				- Input JSON: {6 different object ids}
# 				- Output JSON {success / fail}
# 			- GET:
# 				- Input JSON: {}
# 				- Output JSON {Top 10 results}
				
# 				- Input JSON: {Search terms}
# 				- Output JSON {Result(s)}	

# Analytics:
# 		- Tasks:
# 			- Find the maximum precipitation recorded in the last 5 years (single)			
# 		- Methods: 
# 			- Get
# 				- Input JSON: {field/column, aggregation}
# 				- Output JSON {the aggregated data on the chosen column}		

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

def update(search_terms, new):
    return coll.update_one(search_terms, new)

def bulk_update(search_terms, new_array):
    print ("================ BULK UPDATE ==================")
    print (search_terms)
    print (new_array)
    print ("===============================================")
    return_list = []
    for new in new_array:
        for search_term in search_terms:
            return_list += coll.update_one(search_term, new)
    return return_list

def delete(search_terms):
    return coll.delete_one(search_terms)

def bulk_delete(search_terms):
    return coll.delete_many(search_terms)
