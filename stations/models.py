from json import loads
import pymongo
#TO DO:
#   - put and delete methods in the views.py file are outdated and need to be updated to the new methods (weathers/views.py)
#   - Test update a specific weather station longitude and latitude (single) (and screencap the result)
#   - Remove the long comment (below)
#   - Check that all the methods are standardised between files (more important for this one)
# Stations:
# 		- Tasks:
# 			- Insert a new weather station (single) -- DONE
# 			- Update a specific weather station longitude and latitude (single) -- UNTESTED	
# 		- Methods: 			
# 			- Post:			
# 				- Input JSON: {new weather station} -- DONE
# 				- Output JSON: {success / fail}	-- DONE
# 			- PATCH:
# 				- Input JSON: {weather station & new values} -- UNSURE
# 				- Output JSON: {success / fail} -- UNSURE
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

def station_trigger():
    count = coll.count_documents({})
    if count < 10:
        for i in range(10 - count):
            dummy = {
                        "Device ID": "00_" + str(i),
                        "Latitude": 0,
                        "Longitude": 0,
                        "state": "NSW",
                        "Device Name": "Dummy Station"
                    }
            coll.insert_one(station(dummy))
