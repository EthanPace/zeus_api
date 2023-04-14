from bson.objectid import ObjectId
import pymongo

#TO DO:
#   - put and delete methods in the views.py file are outdated and need to be updated to the new methods (weathers/views.py)
#   - Test update a specific weather station longitude and latitude (single) (and screencap the result)
#   - Check that all the methods are standardised between files (more important for this one)

client = pymongo.MongoClient("mongodb+srv://testUser:testPassword@nasadata.dpq7x0s.mongodb.net/test")
db = client['weatherDataDB']
coll = db['stations']

def station(json_object):
    new_record = {}
    for key in json_object:
        new_record[key] = json_object[key]
    return new_record

def find(search = "", limit = 10):
    if search == "":
        return coll.find().limit(limit)
    else:
        return coll.find({"_id":ObjectId(search)}).limit(limit)

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

