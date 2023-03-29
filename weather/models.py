from json import loads
import pymongo

client = pymongo.MongoClient("mongodb+srv://testUser:testPassword@nasadata.dpq7x0s.mongodb.net/test")
db = client['weatherDataDB']
coll = db['weather']

def weather(json_object):
    new_record = {
        'Time': json_object['Time'],
        'Device ID': json_object['Device ID'],
        'Device Name': json_object['Device Name'],
        'Latitude': json_object['Latitude'],
        'Longitude': json_object['Longitude'],
        'Temperature (°C)': json_object['Temperature (°C)'],
        'Atmospheric Pressure (kPa)': json_object['Atmospheric Pressure (kPa)'],
        'Lightning Average Distance (km)': json_object['Lightning Average Distance (km)'],
        'Lightning Strike Count': json_object['Lightning Strike Count'],
        'Maximum Wind Speed (m/s)': json_object['Maximum Wind Speed (m/s)'],
        'Precipitation mm/h': json_object['Precipitation mm/h'],
        'Solar Radiation (W/m2)': json_object['Solar Radiation (W/m2)'],
        'Vapor Pressure (kPa)': json_object['Vapor Pressure (kPa)'],
        'Humidity (%)': json_object['Humidity (%)'],
        'Wind Direction (°)': json_object['Wind Direction (°)'],
        'Wind Speed (m/s)': json_object['Wind Speed (m/s)']
    }
    return new_record

def find(limit):
    return coll.find().limit(int(limit))
    
def search(search_terms):
    return coll.find_one(search_terms)

def create(new):
    return coll.insert_one(weather(new))

def bulk_create(new_array):
    object_list = []
    for new in new_array:
        object_list += weather(new)
    return coll.insert_many(object_list)

def delete(search_terms):
    return coll.delete_one(search_terms)

def bulk_delete(search_terms):
    return coll.delete_many(search_terms)