from json import loads
from bson.json_util import dumps
import pymongo
#TO DO:
#    - Add working aggregation pipeline to the get_aggregation function
#    - Clear out comments and unused code
#Analytics:
#		- Tasks:
#			- Find the maximum precipitation recorded in the last 5 years (single) -- TO DO		
#		- Methods: 
#			- Get
#				- Input JSON: {field/column, aggregation} -- TO DO
#				- Output JSON {the aggregated data on the chosen column} -- TO DO

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
