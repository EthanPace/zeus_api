from json import loads
from bson.json_util import dumps
import pymongo

client = pymongo.MongoClient("mongodb+srv://testUser:testPassword@nasadata.dpq7x0s.mongodb.net/test")
db = client['weatherDataDB']
coll = db['NSWWeatherData']

#Get_aggregation
#Returns the aggregated data on the chosen column
#Parameters: field, aggregation
def get_max():
    pipeline = [
        {"$group": {"_id": "$Device ID", "maximum_precipitation": {"$max": "$Precipitation mm/h"}}},
        {"$sort": {"max": -1}},
    ]
    return coll.aggregate(pipeline)
